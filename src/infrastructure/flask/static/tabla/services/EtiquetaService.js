/*
Path: services/EtiquetaService.js
*/

import ApiService from './ApiService.js';

class EtiquetaService extends ApiService {
    constructor() {
        super();
    }

    async getEtiquetas() {
        return await this.get('/etiquetas');
    }

    async createEtiqueta(etiquetaData) {
        return await this.post('/etiquetas', etiquetaData);
    }
}

export default EtiquetaService;
