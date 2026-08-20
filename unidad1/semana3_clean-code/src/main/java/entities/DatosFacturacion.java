package entities;

import java.util.List;

// Santiago Octavio Varela / @santiagovOK (GitHub) <santiago.varela@tupad.utn.edu.ar>

public class DatosFacturacion {
    private final List<EstudioMedico> estudios;
    private final boolean esProfesional;
    private final boolean tieneObraSocial;
    private final int cantidadTurnos;

    public DatosFacturacion(List<EstudioMedico> estudios, boolean esProfesional, boolean tieneObraSocial, int cantidadTurnos) {
        this.estudios = estudios;
        this.esProfesional = esProfesional;
        this.tieneObraSocial = tieneObraSocial;
        this.cantidadTurnos = cantidadTurnos;
    }

    public List<EstudioMedico> getEstudios() {
        return estudios;
    }

    public boolean isProfesional() {
        return esProfesional;
    }

    public boolean tieneObraSocial() {
        return tieneObraSocial;
    }

    public int getCantidadTurnos() {
        return cantidadTurnos;
    }
}
