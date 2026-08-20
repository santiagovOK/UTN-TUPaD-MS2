package entities;

// Santiago Octavio Varela / @santiagovOK (GitHub) <santiago.varela@tupad.utn.edu.ar>

public class Paciente {
    private final String nombre;
    private final boolean esProfesional;

    public Paciente(String nombre, boolean esProfesional) {
        this.nombre = nombre;
        this.esProfesional = esProfesional;
    }

    public String getNombre() {
        return nombre;
    }

    public boolean isProfesional() {
        return esProfesional;
    }
}
