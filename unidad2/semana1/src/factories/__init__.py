"""
Módulo de fábricas.

Al igual que con el módulo de reportes, se utiliza este archivo 
como fachada para simplificar las importaciones del resto del sistema.
"""

from .report_factory import ReportFactory

__all__ = ["ReportFactory"]