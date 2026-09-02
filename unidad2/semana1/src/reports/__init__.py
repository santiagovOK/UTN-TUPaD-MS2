"""
Módulo de reportes (Productos del Factory Method).

Nota sobre diseño (Java-ismos):
Se ha decidido mantener deliberadamente la estructura de "una clase por archivo" 
(pdf_report.py, excel_report.py, etc.) propia de Java, a pesar de que la guía sobre java-ismos usada en Programación 4 indica que agrupar clases pequeñas afines en un solo archivo es más idiomático. 

Para mitigar esta fragmentación hacia el exterior, este archivo actúa como fachada.
Permite importar todas las clases directamente desde el paquete `src.reports`, 
ocultando la estructura interna de un archivo por clase.
"""

from .report import Report
from .pdf_report import PDFReport
from .excel_report import ExcelReport
from .csv_report import CSVReport
from .html_report import HTMLReport

__all__ = [
    "Report",
    "PDFReport",
    "ExcelReport",
    "CSVReport",
    "HTMLReport",
]