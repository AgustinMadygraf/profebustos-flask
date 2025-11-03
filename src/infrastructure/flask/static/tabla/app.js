/*
Path: app.js
*/

import ConversionService from './services/ConversionService.js';
import EtiquetaService from './services/EtiquetaService.js';
import ConversionTableComponent from './components/ConversionTableComponent.js';
import EtiquetaTableComponent from './components/EtiquetaTableComponent.js';
import EtiquetaModalComponent from './components/EtiquetaModalComponent.js';

class App {
    constructor() {
        this.conversionService = new ConversionService();
        this.etiquetaService = new EtiquetaService();
        this.conversionTable = new ConversionTableComponent('conversiones-table', 'error-message');
        this.etiquetaTable = new EtiquetaTableComponent('etiquetas-table', 'error-etiquetas');
        this.etiquetaModal = new EtiquetaModalComponent('modalEtiqueta', 'form-etiqueta', 'error-insertar-etiqueta');
        
        this.init();
    }

    async init() {
        await this.loadConversiones();
        await this.loadEtiquetas();
        this.setupEventListeners();
    }

    async loadConversiones() {
        try {
            const conversiones = await this.conversionService.getConversiones();
            this.conversionTable.render(conversiones);
        } catch (error) {
            this.conversionTable.showError('Error al cargar conversiones');
        }
    }

    async loadEtiquetas() {
        try {
            const etiquetas = await this.etiquetaService.getEtiquetas();
            this.etiquetaTable.render(etiquetas);
        } catch (error) {
            this.etiquetaTable.showError('Error al cargar etiquetas');
        }
    }

    setupEventListeners() {
        // Delegamos el manejo del formulario al componente modal
        this.etiquetaModal.setOnSubmit(async (etiquetaData) => {
            try {
                const result = await this.etiquetaService.createEtiqueta(etiquetaData);
                if (result.success) {
                    this.etiquetaModal.close();
                    await this.loadEtiquetas();
                } else {
                    this.etiquetaModal.showError(result.error || 'Error al insertar etiqueta');
                }
            } catch (error) {
                this.etiquetaModal.showError('Error de red al insertar etiqueta');
            }
        });
    }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new App();
});
