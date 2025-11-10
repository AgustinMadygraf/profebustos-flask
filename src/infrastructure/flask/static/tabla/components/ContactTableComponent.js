/*
Path: components/ContactTableComponent.js
*/

import TableComponent from './TableComponent.js';
import DateFormatter from '../utils/DateFormatter.js';

class ContactTableComponent extends TableComponent {
    constructor(tableId, errorElementId) {
        super(tableId, errorElementId);
    }

    renderRow(contacto) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${contacto.ticket_id || ''}</td>
            <td>${contacto.name || ''}</td>
            <td>${contacto.email || ''}</td>
            <td>${contacto.company || ''}</td>
            <td>${contacto.message || ''}</td>
            <td>${contacto.page_location || ''}</td>
            <td>${contacto.traffic_source || ''}</td>
            <td>${contacto.ip || ''}</td>
            <td>${contacto.user_agent || ''}</td>
            <td>${contacto.created_at ? DateFormatter.toBuenosAiresDateTime(contacto.created_at) : ''}</td>
        `;
        return row;
    }
}

export default ContactTableComponent;
