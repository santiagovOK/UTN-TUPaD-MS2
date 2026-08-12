package Notificador;

// Santiago Octavio Varela / @santiagovOK (GitHub) <santiago.varela@tupad.utn.edu.ar>

// 3. Clase de Alto Nivel (Gestor de Negocio - Dependencia en Abstracción)
// Esta clase ahora depende de la interfaz Notificación (Abstracción) y no de clases concretas.

public class GestorTurnos {
    private Notificacion notificacion; // Dependencia por Abstracción

    // Inyección de dependencia (Constructor Injection)
    public GestorTurnos(Notificacion notificacion) {
        this.notificacion = notificacion;
    }

    public void gestionarTurno(String mensaje) {
        // El gestor delega la responsabilidad de 'cómo' notificar.
        // No sabe si es Email, SMS o WhatsApp.
        this.notificacion.enviar(mensaje);

        // ... lógica de negocio de gestión de turnos ...
    }
}