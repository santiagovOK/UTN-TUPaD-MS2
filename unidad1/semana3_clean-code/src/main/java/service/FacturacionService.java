package service;

import entities.DatosFacturacion;
import entities.EstudioMedico;

import java.util.List;

// Santiago Octavio Varela / @santiagovOK (GitHub) <santiago.varela@tupad.utn.edu.ar>

public class FacturacionService {

    public double calcularFacturaTotal(DatosFacturacion datos) {
        if (datos == null || datos.getEstudios() == null || datos.getEstudios().isEmpty()) {
            throw new IllegalArgumentException("Los datos de facturacion y la lista de estudios no pueden ser nulos ni estar vacios");
        }

        double subtotal = sumarEstudiosConDescuento(datos.getEstudios(), datos.isProfesional());
        subtotal = aplicarDescuentoObraSocial(subtotal, datos.tieneObraSocial());
        subtotal = aplicarDescuentoTurnos(subtotal, datos.getCantidadTurnos());

        return Math.round(subtotal * 100.0) / 100.0;
    }

    private double sumarEstudiosConDescuento(List<EstudioMedico> estudios, boolean esProfesional) {
        double resultado = 0;
        for (EstudioMedico estudio : estudios) {
            if (esProfesional) {
                resultado += estudio.getPrecio() * 0.5;
            } else {
                resultado += estudio.getPrecio();
            }
        }
        return resultado;
    }

    private double aplicarDescuentoObraSocial(double subtotal, boolean tieneObraSocial) {
        if (tieneObraSocial) {
            return subtotal * 0.9;
        }
        return subtotal;
    }

    private double aplicarDescuentoTurnos(double subtotal, int cantidadTurnos) {
        if (cantidadTurnos > 3) {
            return subtotal - 100;
        }
        return subtotal;
    }
}
