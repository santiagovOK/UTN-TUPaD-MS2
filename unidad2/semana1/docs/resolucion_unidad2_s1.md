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
│   └── report_factory.py   # Creador (Fábrica estática - nuevo)
├── services/
│   ├── __init__.py
│   └── report_service.py   # Servicio agnóstico al formato (refatorización principal) 
└── main.py                 # Punto de entrada / Cliente (nuevo)
```

El beneficio arquitectónico es que, de ahora en adelante, el `ReportService` no se tocará nunca más cuando haya que agregar un nuevo formato. Solo se creará la nueva clase de reporte y se agregará una línea en el `ReportFactory`.

---

## 4. Código Refactorizado: Implementación

A continuación se desarrolla el código de cada componente del patrón. Se intentará evitar también los "java-ismos" que estamos viendo en programación 4, aunque la idea es priorizar una implementación similar a la establecida en "## Pseudocódigo de la solución" dentro de [docs/consignas](/docs/consignas.md)

### Módulo de reportes (Productos del Factory Method).

**Nota sobre diseño (Java-ismos):** Se ha decidido mantener deliberadamente la estructura de "una clase por archivo"  (pdf_report.py, excel_report.py, etc.) propia de Java, a pesar de que la [guía](/docs/javaismos_guia.md) indica que agrupar clases pequeñas afines en un solo archivo es más idiomático. 

#### `src/reports/report.py` (Interfaz - Nuevo)

Comenzamos definiendo la clase base abstracta `Report`. Esta clase establece el contrato que todos los reportes concretos deben respetar, permitiendo el polimorfismo. No hay un "antes y después" porque se trata de una clase nueva, aunque en parte va a tener relación con la explicación cuando vivia todo en `ReportService`.

```python
from abc import ABC, abstractmethod
from typing import Any

class Report(ABC):
    """
    Interfaz / Clase base abstracta para todos los reportes.
    Centraliza el contrato que consume el ReportService.
    """
    
    @abstractmethod
    def set_data(self, data: Any) -> None:
        pass
        
    @abstractmethod
    def add_header(self, text: str) -> None:
        pass
        
    @abstractmethod
    def add_footer(self, text: str) -> None:
        pass
        
    @abstractmethod
    def render(self) -> None:
        pass
        
    @abstractmethod
    def get_output(self) -> str:
        pass
```

> **Nota sobre Python vs Java:** 
> Siguiendo el manual [*De Java a Python*](/docs/javaismos_guia.md), los métodos `set_data` y `get_output` son lo que se consideraría un "java-ismo" (getters/setters preventivos). En un código Python idiomático desde cero, estos se implementarían como un atributo directo o una `@property` (ej. `@property def output(self) -> str:`). 
> Sin embargo, para cumplir **estrictamente** con el contrato exigido por el pseudocódigo de la consigna (que dicta que `ReportService` llama a `report.set_data(data)` y `report.get_output()`), conservé las firmas originales como métodos. Se utiliza el módulo `abc` y *type hints* para aportar robustez y documentación estática al contrato.

#### `src/reports/pdf_report.py` (Modificado)

**El Código Original (Antes):**
Antes del refactoring, siguiendo lo que se puede suponer de la primera versión problemática de `ReportService`, los reportes eran clases aisladas sin ninguna relación formal entre sí. Existían por su cuenta y el servicio confiaba a ciegas en que tenían ciertos métodos, no había una abstracción que los unifiquen. Por ejemplo, en Python para `PDFReport`:

```python
class PDFReport:
    def set_data(self, data):
        pass
    def get_output():
        return "PDF"
```

**El Código Refactorizado (Después):**
Ahora, la clase hereda explícitamente de la interfaz `Report`. Además, utilizamos `@override` de la librería `typing` para que herramientas como `mypy` verifiquen que efectivamente estamos cumpliendo y sobrescribiendo un método del padre (simulando la red de seguridad del `@Override` de Java).

```python
from typing import Any, override
from .report import Report

class PDFReport(Report):
    
    @override
    def set_data(self, data: Any) -> None:
        pass  # Lógica de generación PDF
        
    @override
    def add_header(self, text: str) -> None:
        pass
        
    @override
    def add_footer(self, text: str) -> None:
        pass
        
    @override
    def render(self) -> None:
        pass
        
    @override
    def get_output(self) -> str:
        return "Contenido PDF"
```

#### `src/reports/excel_report.py` y `src/reports/csv_report.py` (Modificados)

Al igual que con el PDF, estas clases preexistentes se modifican únicamente en su declaración para heredar de la nueva interfaz `Report`, y se decoran sus métodos. La estructura interna es idéntica a `PDFReport`, variando lógicamente solo en el string de retorno y la lógica interna (que acá abstraemos con `pass`).

```python
from typing import Any, override
from .report import Report

class ExcelReport(Report):
    # ... (mismos métodos con @override que en PDFReport) ...
    @override
    def get_output(self) -> str:
        return "Contenido EXCEL"

class CSVReport(Report):
    # ... (mismos métodos con @override que en PDFReport) ...
    @override
    def get_output(self) -> str:
        return "Contenido CSV"
```

#### `src/reports/html_report.py` (Nuevo)

Esta es la evidencia de que el patrón funciona. Agregar este cuarto formato requerido por la consigna implica crear este nuevo archivo y clase, **sin tocar la lógica que consume los reportes**.

```python
from typing import Any, override
from .report import Report

class HTMLReport(Report):
    
    @override
    def set_data(self, data: Any) -> None:
        pass
        
    @override
    def add_header(self, text: str) -> None:
        pass
        
    @override
    def add_footer(self, text: str) -> None:
        pass
        
    @override
    def render(self) -> None:
        pass
        
    @override
    def get_output(self) -> str:
        return "<html>Contenido HTML</html>"
```

### Módulo de fábricas (El Creador)

#### `src/factories/report_factory.py` (Nuevo)

**El Código Original (Antes):**
No existía para este caso puntual. Toda la lógica de decisión (el gran bloque de `if/else` que evaluaba el string `"pdf"`, `"excel"`, etc.) estaba fuertemente acoplada dentro del método `generate` del `ReportService`.

**El Código Refactorizado (Después):**
Se extrae esa responsabilidad a este nuevo componente. Ahora, el único lugar que conoce qué clases concretas existen es esta fábrica.

```python
from src.reports import Report, PDFReport, ExcelReport, CSVReport, HTMLReport

class ReportFactory:
    
    @staticmethod
    def create(format_type: str) -> Report:
        """
        Centraliza la decisión de instanciación de los reportes.
        Si se agrega un formato nuevo, solo se modifica este método.
        """
        format_lower = format_type.lower()
        
        if format_lower == "pdf":
            return PDFReport()
        elif format_lower == "excel":
            return ExcelReport()
        elif format_lower == "csv":
            return CSVReport()
        elif format_lower == "html":
            return HTMLReport()
        else:
            raise ValueError(f"Formato no soportado: {format_type}")
```

> **Nota sobre diseño (Java-ismos):** 
> Aquí se implementa un "java-ismo" estructural de forma adrede para calcar el pseudocódigo (`CLASE ReportFactory: MÉTODO ESTÁTICO create`). Se mantuvo la envoltura de la clase con `@staticmethod` exclusivamente para respetar fielmente la directiva del pseudocódigo de la consigna.

### Módulo de servicios (El Consumidor / Cliente)

#### `src/services/report_service.py` (Refactorización Principal)

**El Código Original (Antes):**
Este es el código problemático traducido a Python. El servicio está fuertemente acoplado a las implementaciones concretas. Cada vez que haya un formato nuevo (como el HTML), **este código debería modificarse**, violando el principio Abierto/Cerrado ("Open/Closed Principle").

```python
# Importaciones rígidas y acopladas
from src.reports.pdf_report import PDFReport
from src.reports.excel_report import ExcelReport
from src.reports.csv_report import CSVReport
from datetime import date
from typing import Any

class ReportService:
    
    def generate(self, data: Any, format_type: str) -> str:
        # MAL: Decisión de construcción mezclada con lógica de uso
        format_lower = format_type.lower()
        if format_lower == "pdf":
            report = PDFReport()
        elif format_lower == "excel":
            report = ExcelReport()
        elif format_lower == "csv":
            report = CSVReport()
        else:
            raise ValueError("Formato no soportado")
            
        # Lógica de uso
        report.set_data(data)
        report.add_header("Reporte Mensual")
        report.add_footer("Generado el " + str(date.today()))
        report.render()
        
        return report.get_output()
```

**El Código Refactorizado (Después):**
Se elimina toda la lógica de instanciación delegándola a la `ReportFactory`. Ahora el servicio es completamente agnóstico al formato concreto; solo habla con la interfaz `Report`. 
Si agregamos el `HTMLReport` los formatos adicionales que se nos puedan ocurrir, **esta clase no se toca más**.

```python
from datetime import date
from typing import Any
from src.factories import ReportFactory
# Ya no importa PDFReport ni ningún otro directamente.

class ReportService:
    
    def generate(self, data: Any, format_type: str) -> str:
        # BIEN: La decisión de instanciación se delegó a la fábrica
        report = ReportFactory.create(format_type)
        
        # La lógica de uso se mantiene intacta, hablando con la abstracción
        report.set_data(data)
        report.add_header("Reporte Mensual")
        report.add_footer("Generado el " + str(date.today()))
        report.render()
        
        return report.get_output()
```

> **Nota sobre diseño (Java-ismos):** 
> Siguiendo lo mencionado en la interfaz `Report`, las llamadas a `report.set_data(data)` y `report.get_output()` dentro de la lógica del servicio se conservaron como métodos tradicionales. En Python idiomático, esto sería `report.data = data` y `return report.output` usando propiedades. La decisión de mantener el paradigma estilo-Java se debe estrictamente a la restricción de la consigna: "La firma pública generate(data, format_type) no puede cambiar" y al intento de hacer coincidir línea por línea la lógica de uso del pseudocódigo proporcionado.

### Punto de entrada (El Cliente Final)

#### `src/main.py` (Nuevo)

Este archivo representa al consumidor final de la aplicación. Aquí es donde se evidencian los beneficios arquitectónico de la refactorización. El cliente puede solicitar el nuevo formato `"html"` requerido por la consigna, y el sistema lo procesa sin que hayamos tenido que modificar el código del `ReportService`.

El cliente solo necesita conocer el servicio. La fábrica y los reportes concretos quedan encapsulados como un detalle de implementación interno del sistema.

```python
from src.services import ReportService

def main() -> None:
    # 1. Instanciamos el servicio (único punto de contacto del cliente)
    servicio = ReportService()
    
    # 2. Preparamos datos simulados
    datos = {
        "empresa": "UTN",
        "ingresos": 1500000,
        "gastos": 800000
    }
    
    print("=== Generando reportes con Factory Method ===\n")
    
    try:
        # Demostración 1: Formato original existente
        print("Solicitando formato PDF.")
        output_pdf = servicio.generate(datos, "pdf")
        print(f"Resultado:\n{output_pdf}\n")
        
        # Demostración 2: Nuevo formato
        # Funciona inmediatamente gracias a que `ReportFactory` lo sabe instanciar.
        # `ReportService` no tuvo que ser enterado de este cambio.
        print("Solicitando formato HTML (Nuevo).")
        output_html = servicio.generate(datos, "html")
        print(f"Resultado:\n{output_html}\n")
        
        # Demostración 3: Comportamiento ante errores
        print("Solicitando formato inexistente.")
        servicio.generate(datos, "xml")
        
    except ValueError as e:
        print(f"Error capturado correctamente: {e}")

if __name__ == "__main__":
    main()
```