"""
Módulo de servicios.

Actúa como fachada para exponer el `ReportService` al exterior.
"""

from .report_service import ReportService

__all__ = ["ReportService"]