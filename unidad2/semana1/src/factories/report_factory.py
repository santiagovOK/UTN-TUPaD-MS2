"""
Centraliza la decisión de instanciación de los reportes.
Si se agrega un formato nuevo, solo se modifica este método.
"""

from src.reports import Report, PDFReport, ExcelReport, CSVReport, HTMLReport

class ReportFactory:
    
    @staticmethod
    def create(format_type: str) -> Report:
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