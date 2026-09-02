"""
Interfaz / Clase base abstracta para todos los reportes.
Centraliza el contrato que consume el ReportService.
"""

from abc import ABC, abstractmethod
from typing import Any

class Report(ABC):
    
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