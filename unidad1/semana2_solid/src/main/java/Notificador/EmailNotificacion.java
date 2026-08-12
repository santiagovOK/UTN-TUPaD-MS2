package Notificador;

// Santiago Octavio Varela / @santiagovOK (GitHub) <santiago.varela@tupad.utn.edu.ar>

// 2. Implementaciones Concretas (Separación de Responsabilidades - SRP)

class EmailNotificacion implements Notificacion {
    @Override
    public void enviar(String mensaje) {
        // Lógica específica de Email
        System.out.println("Enviando EMAIL: " + mensaje);
    }
}