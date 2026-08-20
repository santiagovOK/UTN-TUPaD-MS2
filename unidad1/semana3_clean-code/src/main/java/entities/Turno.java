package entities;

import java.time.LocalDate;

// Santiago Octavio Varela / @santiagovOK (GitHub) <santiago.varela@tupad.utn.edu.ar>

public class Turno {
    private final LocalDate fechaInicio;
    private final int cantidadTurnos;

    public Turno(LocalDate fechaInicio, int cantidadTurnos) {
        this.fechaInicio = fechaInicio;
        this.cantidadTurnos = cantidadTurnos;
    }

    public LocalDate getFechaInicio() {
        return fechaInicio;
    }

    public int getCantidadTurnos() {
        return cantidadTurnos;
    }
}
