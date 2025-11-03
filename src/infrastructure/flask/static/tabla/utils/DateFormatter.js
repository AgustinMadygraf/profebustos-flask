/*
Path: utils/DateFormatter.js
*/

class DateFormatter {
    static toBuenosAiresDateTime(utcString) {
        const fecha = new Date(utcString);
        return fecha.toLocaleString('es-AR', {
            timeZone: 'America/Argentina/Buenos_Aires',
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
        });
    }
}

export default DateFormatter;
