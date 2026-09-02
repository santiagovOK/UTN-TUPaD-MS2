
"""Implementación concreta para reportes en PDF"""


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