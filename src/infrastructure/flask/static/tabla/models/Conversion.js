/*
Path: models/Conversion.js
*/

class Conversion {
    constructor(id, tipo, timestamp, tiempo_navegacion, seccion, web, fuente_trafico, etiqueta = null) {
        this.id = id;
        this.tipo = tipo;
        this.timestamp = timestamp;
        this.tiempo_navegacion = tiempo_navegacion;
        this.seccion = seccion;
        this.web = web;
        this.fuente_trafico = fuente_trafico;
        this.etiqueta = etiqueta;
    }

    getEtiquetaDisplay() {
        return this.etiqueta 
            ? `${this.etiqueta.nombre} (${this.etiqueta.descripcion || ''})`
            : '';
    }

    getTiempoNavegacionSegundos() {
        if (this.tiempo_navegacion == null || isNaN(this.tiempo_navegacion)) return '';
        return `${(this.tiempo_navegacion / 1000).toFixed(1)} s`;
    }
}

export default Conversion;
