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

    render(data) {
        this.hideError();
        this.clearTable();

        if (!Array.isArray(data)) {
            this.showError(data.error || 'Error al cargar datos');
            return;
        }

        data.forEach(item => {
            const row = this.renderRow(item);
            this.tableElement.appendChild(row);
        });
    }
}

export default TableComponent;
