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
        # Funciona inmediatamente gracias a que ReportFactory lo sabe instanciar.
        # ReportService no tuvo que ser enterado de este cambio.
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