from src.geo_service_adapter import GeoServiceAdapter
from src.client import run_business_logic


def main() -> None:
    # Punto de configuración / entrada:
    # Se reemplaza OldGeoService por GeoServiceAdapter sin tocar la lógica de negocio (client.py)
    geo_service = GeoServiceAdapter()
    run_business_logic(geo_service)


if __name__ == "__main__":
    main()
