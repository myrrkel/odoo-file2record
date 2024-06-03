/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { ListController } from "@web/views/list/list_controller";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { FileUploader } from "@web/views/fields/file_handler";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";
import {Component, onMounted} from "@odoo/owl";

export class RecordFileUploader extends Component {
    file2RecordModels = [];
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.attachmentIdsToProcess = [];
        const rec = this.props.record ? this.props.record.data : false;
        onMounted(async () => {
            const showFile2RecordButton = await this.isFile2RecordButtonVisible();
            if (showFile2RecordButton) {
                this.showFile2RecordButton();
            }
        });
    }

    showFile2RecordButton() {
        let file2RecordButton = $(document.getElementsByClassName('btn-file2record'));
        file2RecordButton.removeClass('d-none');
    }

    async isFile2RecordButtonVisible() {
            return await this.orm.call('file2record.config', 'is_file_to_record_button_visible',
                [this.env.searchModel.resModel],
                {context: {...this.extraContext, ...this.env.searchModel.context},});
        }

    async onFileUploaded(file) {
        const attData = {
            name: file.name,
            mimetype: file.type,
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
            ["", this.attachmentIdsToProcess],
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
            this.showFile2RecordButton();
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

registry.category("views").add("record_file_uploader", RecordFileUploader);


ListController.components = {
    ...ListController.components,
    RecordFileUploader,
};


KanbanController.components = {
    ...KanbanController.components,
    RecordFileUploader,
};
