/*
Path: components/EtiquetaModalComponent.js
*/

class EtiquetaModalComponent {
    constructor(modalId, formId, errorElementId) {
        this.modalElement = document.getElementById(modalId);
        this.formElement = document.getElementById(formId);
        this.errorElement = document.getElementById(errorElementId);
        this.onSubmitCallback = null;

        this.init();
    }

    init() {
        this.formElement.addEventListener('submit', this.handleSubmit.bind(this));
    }

    setOnSubmit(callback) {
        this.onSubmitCallback = callback;
    }

    async handleSubmit(event) {
        event.preventDefault();
        
        const nombre = document.getElementById('nombre-etiqueta').value.trim();
        const descripcion = document.getElementById('descripcion-etiqueta').value.trim();

        this.hideError();

        if (this.onSubmitCallback) {
            await this.onSubmitCallback({ nombre, descripcion });
        }
    }

    showError(message) {
        this.errorElement.textContent = message;
        this.errorElement.classList.remove('d-none');
    }

    hideError() {
        this.errorElement.classList.add('d-none');
    }

    close() {
        const modal = bootstrap.Modal.getInstance(this.modalElement);
        modal.hide();
        this.formElement.reset();
    }
}

export default EtiquetaModalComponent;
