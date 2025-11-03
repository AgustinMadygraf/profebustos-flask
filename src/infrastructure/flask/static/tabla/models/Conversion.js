/*
Path: models/Conversion.js
*/

class Conversion {
    constructor(id, tipo, timestamp, seccion, web, etiqueta = null) {
        this.id = id;
        this.tipo = tipo;
        this.timestamp = timestamp;
        this.seccion = seccion;
        this.web = web;
        this.etiqueta = etiqueta;
    }

    getEtiquetaDisplay() {
        return this.etiqueta 
            ? `${this.etiqueta.nombre} (${this.etiqueta.descripcion || ''})`
            : '';
    }
}

export default Conversion;
