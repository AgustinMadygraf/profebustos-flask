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
        console.info('Inicializando App...');
        this.conversionService = new ConversionService();
        this.etiquetaService = new EtiquetaService();
        this.conversionTable = new ConversionTableComponent('conversiones-table', 'error-message');
        this.etiquetaTable = new EtiquetaTableComponent('etiquetas-table', 'error-etiquetas');
        this.etiquetaModal = new EtiquetaModalComponent('modalEtiqueta', 'form-etiqueta', 'error-insertar-etiqueta');
        
        this.init();
    }

    async init() {
        await this.loadEtiquetas();
        await this.loadConversiones();
        this.setupEventListeners();
    }

    async loadConversiones() {
        console.info('Cargando conversiones...');
        try {
            const conversiones = await this.conversionService.getConversiones();
            this.conversiones = conversiones;
            this.conversionTable.render(conversiones, this.etiquetas || []);
            this.setupEtiquetaSelectorListener();
        } catch (error) {
            console.error('Error al cargar conversiones:', error);
            this.conversionTable.showError('Error al cargar conversiones');
        }
    }

    async loadEtiquetas() {
        console.info('Cargando etiquetas...');
        try {
            const etiquetas = await this.etiquetaService.getEtiquetas();
            this.etiquetas = etiquetas;
            this.etiquetaTable.render(etiquetas);
        } catch (error) {
            console.error('Error al cargar etiquetas:', error);
            this.etiquetaTable.showError('Error al cargar etiquetas');
        }
    }

    setupEtiquetaSelectorListener() {
        const tbody = document.querySelector('#conversiones-table tbody');
        tbody.addEventListener('change', async (e) => {
            if (e.target.classList.contains('etiqueta-selector')) {
                const conversionId = e.target.getAttribute('data-conversion-id');
                const etiquetaId = e.target.value;
                console.info(`Selector de etiqueta cambiado: conversionId=${conversionId}, etiquetaId=${etiquetaId}`);
                if (!etiquetaId) {
                    console.warn('No se seleccionó ninguna etiqueta.');
                    return;
                }
                try {
                    await this.conversionService.asignarEtiqueta(conversionId, etiquetaId);
                    await this.loadConversiones();
                } catch (error) {
                    console.error('Error de red al asignar etiqueta:', error);
                    this.conversionTable.showError('Error de red al asignar etiqueta');
                }
            }
        });
    }

    setupEventListeners() {
        // Delegamos el manejo del formulario al componente modal
        this.etiquetaModal.setOnSubmit(async (etiquetaData) => {
            console.info('Formulario de etiqueta enviado:', etiquetaData);
            try {
                const result = await this.etiquetaService.createEtiqueta(etiquetaData);
                if (result.success) {
                    this.etiquetaModal.close();
                    await this.loadEtiquetas();
                    await this.loadConversiones();
                } else {
                    console.warn('Error al insertar etiqueta:', result.error);
                    this.etiquetaModal.showError(result.error || 'Error al insertar etiqueta');
                }
            } catch (error) {
                console.error('Error de red al insertar etiqueta:', error);
                this.etiquetaModal.showError('Error de red al insertar etiqueta');
            }
        });
    }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new App();
});
