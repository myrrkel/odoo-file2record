/** @odoo-module **/
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { ListController } from "@web/views/list/list_controller";
import { FileUploader } from "@web/views/fields/file_handler";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";
const { Component, useRef, useState, onMounted , onWillUnmount} = owl;

class TextUpload extends Component {
    async setup() {
        super.setup();
        this.state = useState({
            snapshot: "",
        });
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.saveButton = useRef("saveButton");
    }

    async sendText() {
        const action = await this.orm.call(this.props.resModel,
            "create_record_from_text",
            ["", text.value],
            {
                context: this.extraContext,
            });
        this.action.doAction(action);
    }
}
TextUpload.template = "file2record_text.TextUpload";
TextUpload.components = { Dialog, FileUploader };

registry.category("fields").add("text_upload", TextUpload);

export class TextFieldController extends Component {

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.dialogService = useService("dialog");
        onMounted(async () => {
            const showText2RecordButton = await this.isText2RecordButtonVisible();
            if (showText2RecordButton) {
                this.showText2RecordButton();
            }
        });
    }

    showText2RecordButton() {
        let text2RecordButton = $(document.getElementsByClassName('btn-text2record'));
        text2RecordButton.removeClass('d-none');
    }

    async isText2RecordButtonVisible() {
        return await this.orm.call('file2record.config', 'is_text_to_record_button_visible',
            [this.env.searchModel.resModel],
            {context: {...this.extraContext, ...this.env.searchModel.context},});
    }

    _openTextController(ev) {
        this.dialogService.add(TextUpload, {
            ...this.props,
            mode: true,
            resModel: this.env.searchModel.resModel,
            onTextCallback: this.onTextCallback,
        });
    }

    async onTextCallback(base64) {
        this.props.update(base64);
    }
}

TextFieldController.template = "file2record_text.TextFieldController"

ListController.components = {
    ...ListController.components,
    TextUpload,
    TextFieldController,
    Dialog,
};

KanbanController.components = {
    ...KanbanController.components,
    TextUpload,
    TextFieldController,
    Dialog,
};


registry.category("fields").add("upload_text_field", TextFieldController);