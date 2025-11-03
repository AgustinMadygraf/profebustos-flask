/*
Path: components/ConversionTableComponent.js
*/

import TableComponent from './TableComponent.js';
import DateFormatter from '../utils/DateFormatter.js';

class ConversionTableComponent extends TableComponent {
    constructor(tableId, errorElementId) {
        super(tableId, errorElementId);
    }

    renderRow(conversionData, etiquetas = []) {
        const tr = document.createElement('tr');
        let etiquetaCell = '';
        if (conversionData.etiqueta) {
            etiquetaCell = `${conversionData.etiqueta.nombre} (${conversionData.etiqueta.descripcion || ''})`;
        } else {
            // Selector de etiquetas si está vacío
            etiquetaCell = `<select class="form-select form-select-sm etiqueta-selector" data-conversion-id="${conversionData.id}">
                <option value="">Etiquetar...</option>
                ${etiquetas.map(e => `<option value="${e.id}">${e.nombre}</option>`).join('')}
            </select>`;
        }

        tr.innerHTML = `
            <td>${conversionData.id}</td>
            <td>${conversionData.tipo}</td>
            <td>${DateFormatter.toBuenosAiresDateTime(conversionData.timestamp)}</td>
            <td>${conversionData.seccion}</td>
            <td>${conversionData.web || ''}</td>
            <td>${etiquetaCell}</td>
        `;
        return tr;
    }
}

export default ConversionTableComponent;
