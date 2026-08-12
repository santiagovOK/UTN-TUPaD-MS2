package Notificador;

// Santiago Octavio Varela / @santiagovOK (GitHub) <santiago.varela@tupad.utn.edu.ar>

// 4. Uso del Sistema (Cliente)
public class Main {
    public static void main(String[] args) {
        // Ejemplo de uso con Email (Inversión de Control)
        Notificacion emailService = new EmailNotificacion();
        GestorTurnos gestor1 = new GestorTurnos(emailService);
        gestor1.gestionarTurno("Tu turno es mañana a las 10:00 AM.");

        // Ejemplo de uso con WhatsApp (Sin modificar GestorTurnos)
        Notificacion whatsappService = new WhatsappNotificacion();
        GestorTurnos gestor2 = new GestorTurnos(whatsappService);
        gestor2.gestionarTurno("Tu turno es mañana a las 10:00 AM.");
    }
}