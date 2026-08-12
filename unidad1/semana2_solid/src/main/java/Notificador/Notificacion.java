package Notificador;

/*
 *
 * @author Santiago Octavio Varela / @santiagovOK (GitHub)
 * <santiago.varela@tupad.utn.edu.ar>
 */

// 1. Abstracción (Principio OCP / DIP)
interface Notificacion {
    /**
     * Método principal para enviar la notificación.
     * @param mensaje El contenido a enviar al paciente.
     */
    void enviar(String mensaje);
}
