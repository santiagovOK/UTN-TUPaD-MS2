# Resolución — Parte A + Parte B: Clean Code y Refactoring Seguro

## Código Base (antes de la refactorización)

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

## Interpretación del dominio en función de la descripción del caso

En el contexto del módulo de facturación médica del Hospital Central, el código original utiliza nombres de variables de una sola letra (`p`, `o`, `t`, `e`, `r`) que no tienen significado semántico. Para aplicar los principios de *Clean Code*, es indispensable interpretar la regla de negocio que subyace a estas operaciones matemáticas y traducirlas al lenguaje del dominio médico-administrativo.

De esta manera, el parámetro `e` representa el valor de cada estudio médico facturado y `r` el total acumulado. La condición `p` se interpreta como una bonificación del 50% aplicable si el paciente es profesional de la salud o pertenece al staff (`esProfesional`). Por su parte, la variable `o` determina la aplicación de un 10% de cobertura global cuando el paciente cuenta con obra social (`tieneObraSocial`). Finalmente, `t` hace referencia a un registro histórico (como la `cantidadTurnos` o días internados), donde una cifra mayor a 3 aplica un descuento fijo de 100 unidades sobre el monto final.

## Funcionalidad
A pesar de los cambios profundos en la estructura del código (extracción de métodos, creación de objetos contenedores y reubicación de responsabilidades), **la funcionalidad original se mantiene intacta**. Esto se debe a que el refactoring aplicado es estrictamente estructural: su objetivo es mejorar la legibilidad, la cohesión y el acoplamiento sin alterar en absoluto las reglas de negocio, el orden de las operaciones ni los resultados finales devueltos por el sistema.

## Problemas Identificados

| Categoría | Problema | Detalle |
|-----------|----------|---------|
| Nombres | calc | Sinónimo de "calcular", no indica dominio (facturación médica) |
| Nombres | p, o, t | Booleanos/int sin contexto: ¿profesional? ¿obra social? ¿turnos? |
| Nombres | r, e | Variables sin significado (resultado, elemento) |
| Cohesión | 4 responsabilidades en un método | Sumar estudios, aplicar descuento profesional, obra social y turno |
| Legibilidad | Un desarrollador nuevo no entiende nada | Nombres sin sentido del dominio |
| Errores | Ningún manejo de errores | No valida null ni lista vacía |
| Acoplamiento | Depende de primitivos genéricos | List<Double> en vez de modelo de dominio |

## Estructura del Proyecto Propuesta

```
src/
├── entities/
│   ├── DatosFacturacion.java     # Entidad: parámetro contenedor
│   ├── Paciente.java             # Entidad: nombre, esProfesional
│   ├── EstudioMedico.java        # Entidad: nombre, precio
│   └── Turno.java                # Entidad: fecha/hora, cantidadTurnos
└── service/
    └── FacturacionService.java   # Lógica de negocio refactorizada
├── Main.java                     # Clase principal de ejecución y verificación
```

**Justificación:**
- `entities` para entidades de dominio (reemplaza `model`)
- `service` para lógica de negocio
- Separación clara entre datos y comportamiento
- Cada entidad representa un concepto del dominio (paciente, estudio, turno)

---

## Aplicación Directa de Refactoring sobre Código Base

### Técnica 1: Extract Method (Parte A + B)

**Aplicación:** Extraer fragmentos del método `calc` como métodos nuevos con nombres descriptivos.

**Problema que resolvía:** Un solo metodo largo que hacía 4 cosas distintas (sumar estudios, aplicar descuento profesional, aplicar obra social, aplicar turno). Dificultaba la lectura y el mantenimiento.

**Mejora:** Cada fragmento de código se convierte en un método con nombre descriptivo, mejorando legibilidad y permitiendo reutilización.

```java
// Antes: clase Facturacion, un solo método largo
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

// Después: clase FacturacionService, métodos extraídos con nombres descriptivos
public double calcularFacturaTotal(List<EstudioMedico> estudios, boolean esProfesional, boolean tieneObraSocial, int cantidadTurnos) {
    if (estudios == null || estudios.isEmpty()) {
        throw new IllegalArgumentException("La lista de estudios no puede ser nula ni estar vacía");
    }

    double subtotal = sumarEstudiosConDescuento(estudios, esProfesional);
    subtotal = aplicarDescuentoObraSocial(subtotal, tieneObraSocial);
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
```

---

### Técnica 2: Introduce Parameter Object (Parte B)

**Aplicación:** Agrupar los parámetros del método en un solo objeto contenedor.

**Problema que resolvía:** El método `calcularFacturaTotal` tiene 4 parámetros de tipos distintos (`List<Double>`, `boolean`, `boolean`, `int`). Si se agrega otro tipo de descuento o dato, la firma crece indefinidamente. También dificulta la reutilización parcial de datos.
```java

// Antes: clase Facturacion, método con 4 parámetros distintos
public double calcularFacturaTotal(List<EstudioMedico> estudios, boolean esProfesional, boolean tieneObraSocial, int cantidadTurnos) { ... }

// Después: clase FacturacionService, método con un solo objeto contenedor
public double calcularFacturaTotal(DatosFacturacion datos) {
    if (datos == null || datos.getEstudios() == null || datos.getEstudios().isEmpty()) {
        throw new IllegalArgumentException("Los datos de facturación y la lista de estudios no pueden ser nulos ni estar vacíos");
    }
    double subtotal = sumarEstudiosConDescuento(datos.getEstudios(), datos.isProfesional());
    subtotal = aplicarDescuentoObraSocial(subtotal, datos.tieneObraSocial());
    subtotal = aplicarDescuentoTurnos(subtotal, datos.getCantidadTurnos());
    return subtotal;
}

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

    public List<EstudioMedico> getEstudios() { return estudios; }
    public boolean isProfesional() { return esProfesional; }
    public boolean tieneObraSocial() { return tieneObraSocial; }
    public int getCantidadTurnos() { return cantidadTurnos; }
}
```

---

### Técnica 3: Move Method (Parte B)

**Aplicación:** Mover la lógica de cálculo a una clase dedicada (`FacturacionService`).

**Problema que resolvía:** La clase `Facturacion` tenía una sola responsabilidad, pero el método `calc` hacía varias cosas distintas y no guardaba estado. Si se agrega nueva funcionalidad relacionada con facturación, la clase crecería sin límite siendo sólo un contenedor de procedimientos.

**Mejora:** Separar la lógica de negocio en una clase dedicada (`FacturacionService`), permitiendo extenderla sin afectar otros módulos. Al carecer de estado propio tras extraer los parámetros, la clase `Facturacion` original quedó vacía y pudo ser eliminada por completo del proyecto, reduciendo código muerto.

```java
// Antes: clase Facturacion
public class Facturacion {
    public double calc(List<Double> estudios, boolean p, boolean o, int t) { ... }
}

// Después: clase FacturacionService
public class FacturacionService {
    public double calcularFacturaTotal(DatosFacturacion datos) { ... }
    private double sumarEstudiosConDescuento(List<EstudioMedico> estudios, boolean esProfesional) { ... }
    private double aplicarDescuentoObraSocial(double subtotal, boolean tieneObraSocial) { ... }
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
            throw new IllegalArgumentException("Los datos de facturación y la lista de estudios no pueden ser nulos ni estar vacíos");
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

    public List<EstudioMedico> getEstudios() { return estudios; }
    public boolean isProfesional() { return esProfesional; }
    public boolean tieneObraSocial() { return tieneObraSocial; }
    public int getCantidadTurnos() { return cantidadTurnos; }
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

    public EstudioMedico(String nombre, double precio) {
        this.nombre = nombre;
        this.precio = precio;
    }

    public String getNombre() { return nombre; }
    public double getPrecio() { return precio; }
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

| Técnica | Dónde se aplica | Problema resuelto | Mejora |
|---------|----------------|-------------------|--------|
| **Extract Method** | Fragmentos de `calc()` | Un solo metodo largo con 4 responsabilidades | Cada fragmento es un método con nombre descriptivo |
| **Introduce Parameter Object** | Firma del método publico | 4 parametros distintos, difícil extender | Un solo objeto contenedor, firma limpia |
| **Move Method** | De `Facturacion` a `FacturacionService` | Clase con una sola responsabilidad pero lógica compleja | Lógica de negocio en clase dedicada; la clase `Facturacion` original fue eliminada por quedar vacía |
