# Diagrama UML Inicial (Código Problemático)

El siguiente diagrama de clases muestra la situación del sistema antes de aplicar el patrón Factory Method. Como se observa, la clase `ReportService` está fuertemente acoplada a las implementaciones concretas de los reportes (`PDFReport`, `ExcelReport`, `CSVReport`), ya que las instancia directamente en su método `generate`.

```mermaid
classDiagram
    class ReportService {
        +generate(data, format_type)
    }
    
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

    %% Dependencias directas (instanciación y uso)
    ReportService ..> PDFReport : Instancia y usa
    ReportService ..> ExcelReport : Instancia y usa
    ReportService ..> CSVReport : Instancia y usa
```
