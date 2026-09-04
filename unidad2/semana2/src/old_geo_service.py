from typing import Any


class OldGeoService:
    """
    Servicio de geolocalización heredado que utiliza todo el sistema existente.
    Esta clase representa la interfaz y el proveedor previo que no se puede cambiar.
    """

    def get_location(self, ip: str) -> dict[str, Any]:
        """
        Retorna la ubicación como un diccionario plano con claves tradicionales.
        """
        # Simulación de respuesta fija para la IP consultada
        return {
            "lat": -34.6037,
            "lng": -58.3816,
            "city": "Buenos Aires",
            "country": "Argentina",
        }
