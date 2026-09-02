from datetime import date
from typing import Any
from src.factories import ReportFactory

class ReportService:
    
    def generate(self, data: Any, format_type: str) -> str:
        # La decisión de instanciación se delegó a la fábrica
        report = ReportFactory.create(format_type)
        
        # La lógica de uso se mantiene intacta, hablando con la abstracción
        report.set_data(data)
        report.add_header("Reporte Mensual")
        report.add_footer("Generado el " + str(date.today()))
        report.render()
        
        return report.get_output()