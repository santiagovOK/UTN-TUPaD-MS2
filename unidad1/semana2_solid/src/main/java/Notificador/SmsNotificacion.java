package Notificador;

// Santiago Octavio Varela / @santiagovOK (GitHub) <santiago.varela@tupad.utn.edu.ar>

// 2. Implementaciones Concretas (Separación de Responsabilidades - SRP)

class SmsNotificacion implements Notificacion {
    @Override
    public void enviar(String mensaje) {
        // Lógica específica de SMS
        System.out.println("Enviando SMS: " + mensaje);
    }
}