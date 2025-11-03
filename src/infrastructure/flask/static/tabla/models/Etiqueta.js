/*
Path: models/Etiqueta.js
*/

class Etiqueta {
    constructor(id, nombre, descripcion = '') {
        this.id = id;
        this.nombre = nombre;
        this.descripcion = descripcion;
    }
}

export default Etiqueta;
