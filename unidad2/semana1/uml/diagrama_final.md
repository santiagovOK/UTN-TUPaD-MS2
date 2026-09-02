# Diagrama UML Final (Refactorizado con Static Factory)

El siguiente diagrama de clases ilustra la arquitectura del sistema después de aplicar el patrón Factory Method (en su variante Simple/Static Factory). 

A diferencia del diagrama inicial, `ReportService` ahora está completamente desacoplado de las implementaciones concretas (`PDFReport`, `HTMLReport`, etc.). Toda la lógica de instanciación fue delegada a `ReportFactory`, y el servicio interactúa exclusivamente a través de la abstracción `Report`.

```mermaid
classDiagram
    %% Interfaz / Abstracción
    class Report {
        <<interface>>
        +set_data(data)
        +add_header(text)
        +add_footer(text)
        +render()
        +get_output() String
    }
    
    %% Productos Concretos
    class PDFReport {
        +set_data(data)
        +add_header(text)
        +add_footer(text)
        +render()
        +get_output() String
    }
    class ExcelReport {
        +set_data(data)
        +add_header(text)
        +add_footer(text)
        +render()
        +get_output() String
    }
    class CSVReport {
        +set_data(data)
        +add_header(text)
        +add_footer(text)
        +render()
        +get_output() String
    }
    class HTMLReport {
        +set_data(data)
        +add_header(text)
        +add_footer(text)
        +render()
        +get_output() String
    }

    %% Creador (Static Factory)
    class ReportFactory {
        +create(format_type) Report$
    }

    %% Consumidor
    class ReportService {
        +generate(data, format_type)
    }

    %% Relaciones de Dependencia y Uso
    ReportFactory ..> PDFReport : Instancia
    ReportFactory ..> ExcelReport : Instancia
    ReportFactory ..> CSVReport : Instancia
    ReportFactory ..> HTMLReport : Instancia
    
    ReportService ..> ReportFactory : Usa para crear
    
    %% Relaciones de Herencia y Abstracción apuntando a Report 
    %% (Invertir el sentido de la escritura forza a Mermaid a aislar el nodo principal en un extremo)
    PDFReport ..|> Report : Implementa
    ExcelReport ..|> Report : Implementa
    CSVReport ..|> Report : Implementa
    HTMLReport ..|> Report : Implementa
    ReportFactory ..> Report : Retorna
    ReportService ..> Report : Usa
```
