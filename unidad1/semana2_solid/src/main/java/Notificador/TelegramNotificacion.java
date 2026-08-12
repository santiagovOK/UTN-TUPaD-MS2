package Notificador;

// Santiago Octavio Varela / @santiagovOK (GitHub) <santiago.varela@tupad.utn.edu.ar>

// Parte C — Extensibilidad
public class TelegramNotificacion implements Notificacion {
    @Override
    public void enviar(String mensaje) {
        // Lógica específica de Telegram
        System.out.println("Enviando TELEGRAM: " + mensaje);
    }
}
