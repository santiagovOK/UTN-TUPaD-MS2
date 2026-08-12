package Notificador;

// Santiago Octavio Varela / @santiagovOK (GitHub) <santiago.varela@tupad.utn.edu.ar>

// Parte C — Extensibilidad
public class PushNotificacion implements Notificacion {
    @Override
    public void enviar(String mensaje) {
        // Lógica específica de Push notifications
        System.out.println("Enviando PUSH: " + mensaje);
    }
}