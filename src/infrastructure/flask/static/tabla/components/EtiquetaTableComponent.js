/*
Path: components/EtiquetaTableComponent.js
*/

import TableComponent from './TableComponent.js';

class EtiquetaTableComponent extends TableComponent {
    constructor(tableId, errorElementId) {
        super(tableId, errorElementId);
    }

    renderRow(etiquetaData) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${etiquetaData.id}</td>
            <td>${etiquetaData.nombre}</td>
            <td>${etiquetaData.descripcion || ''}</td>
        `;
        return tr;
    }
}

export default EtiquetaTableComponent;
