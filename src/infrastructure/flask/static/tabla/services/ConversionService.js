/*
Path: services/ApiService.js
*/

import ApiService from './ApiService.js';

class ConversionService extends ApiService {
    constructor() {
        super();
    }

    async getConversiones() {
        return await this.get('/conversiones');
    }

    async asignarEtiqueta(conversionId, etiquetaId) {
        return await this.post(`/conversiones/${conversionId}/etiqueta`, { etiqueta_id: etiquetaId });
    }
}

export default ConversionService;
