/** @odoo-module **/

import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {ListController} from "@web/views/list/list_controller";
import {KanbanController} from "@web/views/kanban/kanban_controller";
import {FileUploader} from "@web/views/fields/file_handler";
import {standardWidgetProps} from "@web/views/widgets/standard_widget_props";
import {Component, onWillStart} from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { user } from "@web/core/user";


export class RecordFileUploader extends Component {
    static template = 'file2record.RecordFileUploader';
    static components = {
        FileUploader,
    };
    static props = {record: {type: Object, optional: true}}

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.attachmentIdsToProcess = [];
        const rec = this.props.record ? this.props.record.data : false;
    }

    async onFileUploaded(file) {
        const attData = {
            name: file.name,
            mimetype: file.type,
            type: 'binary',
            datas: file.data,
            res_model: this.env.searchModel.resModel,
        };
        const attId = await this.orm.create("ir.attachment", [attData], {
            context: { ...this.extraContext, ...this.env.searchModel.context },
        });
        this.attachmentIdsToProcess.push(attId);
    }

    async onUploadComplete() {
        const action = await this.orm.call(this.env.searchModel.resModel,
            "create_records_from_attachments",
            [this.attachmentIdsToProcess],
            {
                context: {...this.extraContext, ...this.env.searchModel.context},
            });
        this.attachmentIdsToProcess = [];
        if (action.context && action.context.notifications) {
            for (let [file, msg] of Object.entries(action.context.notifications)) {
                this.notification.add(
                    msg,
                    {
                        title: file,
                        type: "info",
                        sticky: true,
                    });
            }
            delete action.context.notifications;
            this.action.doAction(action);
        } else {
            if (action) {
                this.action.doAction(action);
            }
            else {
                this.notification.add(this.env._t("Could not extract data from file"), {
                    type: "danger",
                });
            }
        }
    }
}

RecordFileUploader.components = {
    FileUploader,
};
RecordFileUploader.template = "file2record.RecordFileUploader";
RecordFileUploader.extractProps = ({ attrs }) => ({
    togglerTemplate: attrs.template || "",
    btnClass: attrs.btnClass || "",

});
RecordFileUploader.props = {
    ...standardWidgetProps,
    record: { type: Object, optional: true},
    togglerTemplate: { type: String, optional: true },
    btnClass: { type: String, optional: true },
    linkText: { type: String, optional: true },
    slots: { type: Object, optional: true },
}

RecordFileUploader.fieldDependencies = {
    id: { type: "integer" },
    type: { type: "selection" },
};

async function _isFile2RecordButtonVisible(self) {
    if (!await user.hasGroup("file2record.group_file_upload_user") || !self.props.resModel) {
        return false;
    }
    try {
        return self.orm.call(
            self.props.resModel,
            "is_file_to_record_button_visible",
            [],
            {
                context: {...self.extraContext, ...self.env.searchModel.context},
            }
        );
    } catch (error) {
        return false;
    }
}

ListController.components = {
    ...ListController.components,
    RecordFileUploader,
};

export const ListControllerPatch = {
    props: {
        ...ListController.props,
        isUploadButtonVisible: { type: Boolean, optional: true },
    },

    setup() {
        super.setup();
        this.orm = useService("orm");
        onWillStart(async () => {
            try {
                const isVisible = await _isFile2RecordButtonVisible(this);
                this.props.isUploadButtonVisible = isVisible;
            } catch (error) {
                console.error('Error checking file2record button visibility:', error);
                this.props.isUploadButtonVisible = false;
            }
        });
    },
};

patch(ListController.prototype, ListControllerPatch);

KanbanController.components = {
    ...KanbanController.components,
    RecordFileUploader,
};

export const KanbanControllerPatch = {
    props: {
        ...KanbanController.props,
        isUploadButtonVisible: {type: Boolean, optional: true},
    },

    setup() {
        super.setup();
        this.orm = useService("orm");
        onWillStart(async () => {
            try {
                this.props.isUploadButtonVisible = await _isFile2RecordButtonVisible(this);
            } catch (error) {
                this.props.isUploadButtonVisible = false;
            }
        });
    }
}


patch(KanbanController.prototype, KanbanControllerPatch);
