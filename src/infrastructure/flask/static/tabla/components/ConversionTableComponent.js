/*
Path: components/ConversionTableComponent.js
*/

import TableComponent from './TableComponent.js';
import DateFormatter from '../utils/DateFormatter.js';

class ConversionTableComponent extends TableComponent {
    constructor(tableId, errorElementId) {
        super(tableId, errorElementId);
    }

    renderRow(conversionData) {
        const tr = document.createElement('tr');
        const etiquetaDisplay = conversionData.etiqueta
            ? `${conversionData.etiqueta.nombre} (${conversionData.etiqueta.descripcion || ''})`
            : '';

        tr.innerHTML = `
            <td>${conversionData.id}</td>
            <td>${conversionData.tipo}</td>
            <td>${DateFormatter.toBuenosAiresDateTime(conversionData.timestamp)}</td>
            <td>${conversionData.seccion}</td>
            <td>${conversionData.web || ''}</td>
            <td>${etiquetaDisplay}</td>
        `;
        return tr;
    }
}

export default ConversionTableComponent;
