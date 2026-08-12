package Notificador;

// Santiago Octavio Varela / @santiagovOK (GitHub) <santiago.varela@tupad.utn.edu.ar>

// 4. Uso del Sistema (Cliente)
public class Main {
    public static void main(String[] args) {
        // Ejemplo de uso con Email (Inversión de Control)
        Notificacion emailService = new EmailNotificacion();
        GestorTurnos gestor1 = new GestorTurnos(emailService);
        gestor1.gestionarTurno("[Enviado vía EMAIL] Tu turno es mañana a las 10:00 AM.");

        // Ejemplo de uso con WhatsApp (Sin modificar GestorTurnos)
        Notificacion whatsappService = new WhatsappNotificacion();
        GestorTurnos gestor2 = new GestorTurnos(whatsappService);
        gestor2.gestionarTurno("[Enviado vía WHATSAPP] Tu turno es mañana a las 10:00 AM.");

        // Parte C — Extensibilidad (sin modificar GestorTurnos)
        Notificacion telegramService = new TelegramNotificacion();
        GestorTurnos gestor3 = new GestorTurnos(telegramService);
        gestor3.gestionarTurno("[Enviado vía TELEGRAM] Tu turno es mañana a las 10:00 AM.");

        Notificacion pushService = new PushNotificacion();
        GestorTurnos gestor4 = new GestorTurnos(pushService);
        gestor4.gestionarTurno("[Enviado vía PUSH] Tu turno es mañana a las 10:00 AM.");

    }
}