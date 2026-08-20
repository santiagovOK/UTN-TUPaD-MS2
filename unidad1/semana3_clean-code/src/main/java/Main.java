import entities.DatosFacturacion;
import entities.EstudioMedico;
import service.FacturacionService;

import java.util.Arrays;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        FacturacionService service = new FacturacionService();

        List<EstudioMedico> estudios = Arrays.asList(
                new EstudioMedico("Sangre", 1000.0),
                new EstudioMedico("Radiografia", 2000.0)
        );

        // Caso 1: esProfesional=true, tieneObraSocial=true, cantidadTurnos=4
        // Base: 3000
        // esProfesional=true -> 1500
        // tieneObraSocial=true -> 1500 * 0.9 = 1350
        // cantidadTurnos=4 (>3) -> 1350 - 100 = 1250
        DatosFacturacion datos1 = new DatosFacturacion(estudios, true, true, 4);
        double result1 = service.calcularFacturaTotal(datos1);
        System.out.println("Resultado 1: " + result1 + " (Esperado: 1250.0)");

        // Caso 2: esProfesional=false, tieneObraSocial=false, cantidadTurnos=2
        // Base: 3000 -> 3000 -> 3000
        DatosFacturacion datos2 = new DatosFacturacion(estudios, false, false, 2);
        double result2 = service.calcularFacturaTotal(datos2);
        System.out.println("Resultado 2: " + result2 + " (Esperado: 3000.0)");

        if (result1 == 1250.0 && result2 == 3000.0) {
            System.out.println("EXITOSO");
        } else {
            System.err.println("FALLIDO");
            System.exit(1);
        }
    }
}
