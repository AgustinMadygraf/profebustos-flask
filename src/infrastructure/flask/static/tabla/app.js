/*
Path: app.js
*/


import ApiService from './services/ApiService.js';
import ContactTableComponent from './components/ContactTableComponent.js';


class App {
    constructor() {
        console.info('Inicializando App...');
        this.apiService = new ApiService();
        this.contactTable = new ContactTableComponent('contactos-table', 'error-message');
        this.init();
    }

    async init() {
        await this.loadContactos();
    }

    async loadContactos() {
        try {
            const response = await this.apiService.get('/v1/contact/list');
            if (response.success && Array.isArray(response.contactos)) {
                this.contactTable.render(response.contactos);
            } else {
                this.contactTable.showError('No se pudieron cargar los contactos.');
            }
        } catch (error) {
            console.error('Error al cargar contactos:', error);
            this.contactTable.showError('Error al cargar contactos.');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new App();
});
