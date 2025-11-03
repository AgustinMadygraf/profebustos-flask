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
}

export default ConversionService;
