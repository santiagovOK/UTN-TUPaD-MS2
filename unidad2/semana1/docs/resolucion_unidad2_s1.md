# Resolución Unidad 2 - Semana 1: Estructura en Python

## 1. Diagrama UML Inicial

Diagrama UML de clases correspondiente a la situación problemática inicial (antes del refactoring). Este diagrama muestra el acoplamiento directo entre `ReportService` y los distintos reportes concretos (`PDFReport`, `ExcelReport`, `CSVReport`).

👉 **Ver diagrama:** [uml/diagrama_inicial.md](../uml/diagrama_inicial.md)

---

## 2. Variante Elegida: Static Factory

Para esta refactorización en Python se ha elegido la variante **Static Factory** (también conocida como Simple Factory), siguiendo la solución propuesta en el pseudocódigo original (`ReportFactory` con un método estático `create`).

**¿Por qué no se usó el patrón Factory Method canónico (GoF estricto)?**
El patrón estricto de la **Gang of Four** requiere utilizar **herencia**. Esto implicaría transformar `ReportService` en una clase abstracta con un método `createReport()` y luego crear subclases concretas como `PdfReportService`, `ExcelReportService`, etc., donde cada una sobrescriba el método para instanciar su respectivo reporte.

Se decidió no utilizar esta variante estricta porque la lógica de negocio del servicio (el método `generate` que inserta datos, agrega cabeceras y renderiza) es **exactamente la misma** para todos los formatos. Obligarnos a crear una jerarquía paralela de creadores (servicios) únicamente para cambiar la clase que se instancia introduciría una complejidad innecesaria sin aportar ningún valor de comportamiento. La *Static Factory* centraliza esta decisión de forma mucho más limpia, liviana y pragmática para este escenario, que es más sencillo.

---

## 3. Estructura de Archivos

A continuación se presenta la estructura de archivos tentativa para la implementación en Python. En esta etapa solo se definen los esqueletos de las clases y métodos (sin la lógica interna).


```text
src/
├── reports/
│   ├── __init__.py
│   ├── report.py           # Interfaz / Clase base (nuevo)
│   ├── pdf_report.py       # Producto concreto (modificado, implementa Report)
│   ├── excel_report.py     # Producto concreto (modificado, implementa Report)
│   ├── csv_report.py       # Producto concreto (modificado, implementa Report)
│   └── html_report.py      # Producto concreto (nuevo, implementa Report))
├── factories/
│   ├── __init__.py
│   └── report_factory.py   # Creador (Fábrica estática - nuevoç)
├── services/
│   ├── __init__.py
│   └── report_service.py   # Servicio agnóstico al formato (refatorización principal) 
└── main.py                 # Punto de entrada / Cliente (nuevo)
```

El beneficio arquitectónico es que, de ahora en adelante, el `ReportService` no se tocará nunca más cuando haya que agregar un nuevo formato. Solo se creará la nueva clase de reporte y se agregará una línea en el `ReportFactory`.