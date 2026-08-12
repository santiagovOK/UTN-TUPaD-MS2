package Notificador;

// Santiago Octavio Varela / @santiagovOK (GitHub) <santiago.varela@tupad.utn.edu.ar>

// 2. Implementaciones Concretas (Separación de Responsabilidades - SRP)

class WhatsappNotificacion implements Notificacion {
    @Override
    public void enviar(String mensaje) {
        // Lógica específica de WhatsApp
        System.out.println("Enviando WhatsApp: " + mensaje);
    }
}