/** @odoo-module **/
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { ListController } from "@web/views/list/list_controller";
import { FileUploader } from "@web/views/fields/file_handler";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";
const { Component, useRef, useState, onMounted , onWillUnmount} = owl;

class WebcamUpload extends Component {
    async setup() {
        this.state = useState({
            snapshot: "",
        });
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.video = useRef("video");
        this.saveButton = useRef("saveButton");
        this.selectCamera = useRef("selectCamera");
        this.stream = null;
        onWillUnmount(this._onClose);
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({video: true, audio: false});
        } catch (error) {
            alert(error.message);
            return;
        }
        if (video != null) {
            video.srcObject = this.stream;
        }
        else {
            alert("Error getting video stream");
        }
    }

    async takePicture() {
        canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
        let image_data_url = canvas.toDataURL('image/jpeg', 1.0);
        dataurl.value = image_data_url;

        const attData = {
            name: 'camera.jpg',
            mimetype: 'image/jpeg',
            datas: image_data_url.split(",")[1],
            res_model: this.props.resModel,
        };
        const attId = await this.orm.create("ir.attachment", [attData], {
            context: this.extraContext,
        });

        await this.onUploadComplete(attId);
    }

    async _onClose() {
        if (this.stream == null) {
            return;
        }
        await this.stream.getTracks().forEach(track => track.stop());
    }

    async onUploadComplete(att_id) {
        const action = await this.orm.call(this.props.resModel,
            "create_records_from_attachments",
            ["", [att_id]],
            {
                context: this.extraContext,
            });
        this.attachmentIdsToProcess = [];
        if (action.context?.notifications) {
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
        }
        await this._onClose()
        this.action.doAction(action);
    }
}
WebcamUpload.template = "file2record_camera.WebcamUpload";
WebcamUpload.components = { Dialog, FileUploader };

registry.category("fields").add("webcam_upload", WebcamUpload);

export class WebcamImageField extends Component {

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.dialogService = useService("dialog");
        onMounted(async () => {
            const showCamera2RecordButton = await this.isCamera2RecordButtonVisible();
            if (showCamera2RecordButton) {
                this.showCamera2RecordButton();
            }
        });
    }

    showCamera2RecordButton() {
        let camera2RecordButton = $(document.getElementsByClassName('btn-camera2record'));
        camera2RecordButton.removeClass('d-none');
    }

    async isCamera2RecordButtonVisible() {
        return await this.orm.call('file2record.config', 'is_camera_to_record_button_visible',
            [this.env.searchModel.resModel],
            {context: {...this.extraContext, ...this.env.searchModel.context},});
    }

    _openWebcam(ev) {
        this.dialogService.add(WebcamUpload, {
            ...this.props,
            mode: true,
            resModel: this.env.searchModel.resModel,
            onWebcamCallback: this.onWebcamCallback,
        });
    }

    async onWebcamCallback(base64) {
        this.props.update(base64);
    }
}

WebcamImageField.template = "file2record_camera.WebcamImageField"

ListController.components = {
    ...ListController.components,
    WebcamUpload,
    WebcamImageField,
    Dialog,
};

KanbanController.components = {
    ...KanbanController.components,
    WebcamUpload,
    WebcamImageField,
    Dialog,
};


registry.category("fields").add("webcam_image_field", WebcamImageField);