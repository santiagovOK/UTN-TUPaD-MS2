from src.old_geo_service import OldGeoService


def run_business_logic(geo: OldGeoService, ip: str = "200.45.123.10") -> None:
    """
    Simula la lógica de negocio presente en los 40 archivos del sistema.
    Consume exclusivamente la interfaz de OldGeoService sin conocer si por detrás
    se encuentra el servicio original o un Adapter.
    """
    data = geo.get_location(ip)
    print(f"Ciudad: {data['city']}, Latitud: {data['lat']}")
