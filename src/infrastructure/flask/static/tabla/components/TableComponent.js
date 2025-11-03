/*
Path: components/TableComponent.js
*/

class TableComponent {
    constructor(tableId, errorElementId) {
        this.tableElement = document.querySelector(`#${tableId} tbody`);
        this.errorElement = document.getElementById(errorElementId);
    }

    showError(message) {
        this.errorElement.textContent = message;
        this.errorElement.classList.remove('d-none');
    }

    hideError() {
        this.errorElement.classList.add('d-none');
    }

    clearTable() {
        this.tableElement.innerHTML = '';
    }

    // Método abstracto que deben implementar las subclases
    renderRow(data) {
        throw new Error('Método renderRow debe ser implementado por la subclase');
    }

    render(conversiones, etiquetas = []) {
        this.tableElement.innerHTML = '';
        conversiones.forEach(conversion => {
            const row = this.renderRow(conversion, etiquetas);
            this.tableElement.appendChild(row);
        });
    }
}

export default TableComponent;
