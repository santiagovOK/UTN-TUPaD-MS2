# Resolución — Parte A + Parte B: Clean Code y Refactoring Seguro

## Código Base (antes del refactoring)

```java
import java.util.List;

public class Facturacion {

    public double calc(List<Double> estudios,
                       boolean p,
                       boolean o,
                       int t) {

        double r = 0;

        for (Double e : estudios) {

            if (p == true) {
                r += e * 0.5;
            } else {
                r += e;
            }

        }

        if (o == true) {
            r = r * 0.9;
        }

        if (t > 3) {
            r = r - 100;
        }

        return r;

    }

}
```

## Problemas Identificados

| Categoria | Problema | Detalle |
|-----------|----------|---------|
| Nombres | calc | Sinonimo de "calcular", no indica dominio (facturacion medica) |
| Nombres | p, o, t | Booleanos/int sin contexto: ¿profesional? ¿obsoleto? ¿turnos? |
| Nombres | r, e | Variables sin significado (resultado, elemento) |
| Cohesion | 4 responsabilidades en un metodo | Sumar estudios, aplicar descuento profesional, obsolescencia y turno |
| Legibilidad | Un desarrollador nuevo no entiende nada | Nombres sin sentido del dominio |
| Errores | Ningun manejo de errores | No valida null ni lista vacia |
| Acoplamiento | Depende de primitivos genericos | List<Double> en vez de modelo de dominio |

## Estructura del Proyecto Propuesta

```
src/
├── entities/
│   ├── Facturacion.java          # Entidad: codigo base original
│   ├── Paciente.java             # Entidad: nombre, esProfesional
│   ├── EstudioMedico.java        # Entidad: nombre, precio, esObsoleto
│   └── Turno.java                # Entidad: fecha/hora, cantidadTurnos
└── service/
    └── FacturacionService.java   # Lógica de negocio refactorizada
```

**Justificacion:**
- `entities` para entidades de dominio (reemplaza `model`)
- `service` para lógica de negocio
- Separacion clara entre datos y comportamiento
- Cada entidad representa un concepto del dominio (paciente, estudio, turno)

---

## Aplicacion Directa de Refactoring sobre Código Base

### Tecnica 1: Extract Method (Parte A + B)

**Aplicacion:** Extraer fragmentos del metodo `calc` como metodos nuevos con nombres descriptivos.

**Problema que resolvía:** Un solo metodo largo que hacia 4 cosas distintas (sumar estudios, aplicar descuento profesional, aplicar obsolescencia, aplicar turno). Dificultaba la lectura y el mantenimiento.

**Mejora:** Cada fragmento de codigo se convierte en un metodo con nombre descriptivo, mejorando legibilidad y permitiendo reutilizacion.

```java
// Antes: un solo metodo largo
public double calc(List<Double> estudios, boolean p, boolean o, int t) {
    double r = 0;
    for (Double e : estudios) {
        if (p == true) {
            r += e * 0.5;
        } else {
            r += e;
        }
    }
    if (o == true) {
        r = r * 0.9;
    }
    if (t > 3) {
        r = r - 100;
    }
    return r;
}

// Despues: metodos extraidos con nombres descriptivos
public double calcularFacturaTotal(List<EstudioMedico> estudios, boolean esProfesional, boolean esObsoleto, int cantidadTurnos) {
    if (estudios == null || estudios.isEmpty()) {
        throw new IllegalArgumentException("La lista de estudios no puede ser nula ni estar vacia");
    }

    double subtotal = sumarEstudiosConDescuento(estudios, esProfesional);
    subtotal = aplicarDescuentoObsoleto(subtotal, esObsoleto);
    subtotal = aplicarDescuentoTurnos(subtotal, cantidadTurnos);
    return subtotal;
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

private double aplicarDescuentoObsoleto(double subtotal, boolean esObsoleto) {
    if (esObsoleto) {
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
```

---

### Tecnica 2: Introduce Parameter Object (Parte B)

**Aplicacion:** Agrupar los parametros del metodo en un solo objeto contenedor.

**Problema que resolvía:** El metodo `calcularFacturaTotal` tiene 4 parametros de tipos distintos (`List<Double>`, `boolean`, `boolean`, `int`). Si se agrega otro tipo de descuento o dato, la firma crece indefinidamente. Tambien dificulta la reutilizacion parcial de datos.
```java

// Antes: 4 parametros distintos
public double calcularFacturaTotal(List<EstudioMedico> estudios, boolean esProfesional, boolean esObsoleto, int cantidadTurnos) { ... }

// Despues: un solo objeto contenedor con nombres descriptivos
public double calcularFacturaTotal(DatosFacturacion datos) {
    if (datos == null || datos.getEstudios() == null || datos.getEstudios().isEmpty()) {
        throw new IllegalArgumentException("Los datos de facturacion y la lista de estudios no pueden ser nulos ni estar vacios");
    }
    double subtotal = sumarEstudiosConDescuento(datos.getEstudios(), datos.isProfesional());
    subtotal = aplicarDescuentoObsoleto(subtotal, datos.isObsoleto());
    subtotal = aplicarDescuentoTurnos(subtotal, datos.getCantidadTurnos());
    return subtotal;
}

public class DatosFacturacion {
    private final List<EstudioMedico> estudios;
    private final boolean esProfesional;
    private final boolean esObsoleto;
    private final int cantidadTurnos;

    public DatosFacturacion(List<EstudioMedico> estudios, boolean esProfesional, boolean esObsoleto, int cantidadTurnos) {
        this.estudios = estudios;
        this.esProfesional = esProfesional;
        this.esObsoleto = esObsoleto;
        this.cantidadTurnos = cantidadTurnos;
    }

    public List<EstudioMedico> getEstudios() { return estudios; }
    public boolean isProfesional() { return esProfesional; }
    public boolean isObsoleto() { return esObsoleto; }
    public int getCantidadTurnos() { return cantidadTurnos; }
}
```

---

### Tecnica 3: Move Method (Parte B)

**Aplicacion:** Mover la logica de calculo a una clase dedicada (`FacturacionService`).

**Problema que resolvía:** La clase `Facturacion` tenia una sola responsabilidad, pero el metodo `calc` hacia varias cosas distintas. Si se agrega nueva funcionalidad relacionada con facturacion, la clase crece sin limite.

**Mejora:** Separar la logica de negocio en una clase dedicada, permitiendo extenderla sin afectar otros modulos.

```java
// Antes: solo en Facturacion
public class Facturacion {
    public double calc(List<Double> estudios, boolean p, boolean o, int t) { ... }
}

// Despues: mover a FacturacionService
public class FacturacionService {
    public double calcularFacturaTotal(DatosFacturacion datos) { ... }
    private double sumarEstudiosConDescuento(List<EstudioMedico> estudios, boolean esProfesional) { ... }
    private double aplicarDescuentoObsoleto(double subtotal, boolean esObsoleto) { ... }
    private double aplicarDescuentoTurnos(double subtotal, int cantidadTurnos) { ... }
}

```

---

## Código Final Propuesto (Parte A + Parte B combinadas)

```java
// service/FacturacionService.java
public class FacturacionService {

    public double calcularFacturaTotal(DatosFacturacion datos) {
        if (datos == null || datos.getEstudios() == null || datos.getEstudios().isEmpty()) {
            throw new IllegalArgumentException("Los datos de facturacion y la lista de estudios no pueden ser nulos ni estar vacios");
        }

        double subtotal = sumarEstudiosConDescuento(datos.getEstudios(), datos.isProfesional());
        subtotal = aplicarDescuentoObsoleto(subtotal, datos.isObsoleto());
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

    private double aplicarDescuentoObsoleto(double subtotal, boolean esObsoleto) {
        if (esObsoleto) {
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

public class DatosFacturacion {
    private final List<EstudioMedico> estudios;
    private final boolean esProfesional;
    private final boolean esObsoleto;
    private final int cantidadTurnos;

    public DatosFacturacion(List<EstudioMedico> estudios, boolean esProfesional, boolean esObsoleto, int cantidadTurnos) {
        this.estudios = estudios;
        this.esProfesional = esProfesional;
        this.esObsoleto = esObsoleto;
        this.cantidadTurnos = cantidadTurnos;
    }

    public List<EstudioMedico> getEstudios() { return estudios; }
    public boolean isProfesional() { return esProfesional; }
    public boolean isObsoleto() { return esObsoleto; }
    public int getCantidadTurnos() { return cantidadTurnos; }
}

// entities/Facturacion.java (codigo base minimizado)
public class Facturacion {
    // La clase original se mantiene, pero la logica se mueve a FacturacionService
}

// entities/Paciente.java
public class Paciente {
    private final String nombre;
    private final boolean esProfesional;

    public Paciente(String nombre, boolean esProfesional) {
        this.nombre = nombre;
        this.esProfesional = esProfesional;
    }

    public String getNombre() { return nombre; }
    public boolean isProfesional() { return esProfesional; }
}

// entities/EstudioMedico.java
public class EstudioMedico {
    private final String nombre;
    private final double precio;
    private final boolean esObsoleto;

    public EstudioMedico(String nombre, double precio, boolean esObsoleto) {
        this.nombre = nombre;
        this.precio = precio;
        this.esObsoleto = esObsoleto;
    }

    public String getNombre() { return nombre; }
    public double getPrecio() { return precio; }
    public boolean isObsoleto() { return esObsoleto; }
}

// entities/Turno.java
public class Turno {
    private final LocalDate fechaInicio;
    private final int cantidadTurnos;

    public Turno(LocalDate fechaInicio, int cantidadTurnos) {
        this.fechaInicio = fechaInicio;
        this.cantidadTurnos = cantidadTurnos;
    }

    public LocalDate getFechaInicio() { return fechaInicio; }
    public int getCantidadTurnos() { return cantidadTurnos; }
}
```
---

## Resumen de Técnicas Aplicadas

| Tecnica | Donde se aplica | Problema resuelto | Mejora |
|---------|----------------|-------------------|--------|
| **Extract Method** | Fragmentos de `calc()` | Un solo metodo largo con 4 responsabilidades | Cada fragmento es un metodo con nombre descriptivo |
| **Introduce Parameter Object** | Firma del metodo publico | 4 parametros distintos, dificil extender | Un solo objeto contenedor, firma limpia |
| **Move Method** | De `Facturacion` a `FacturacionService` | Clase con una sola responsabilidad pero logica compleja | Logica de negocio en clase dedicada |
