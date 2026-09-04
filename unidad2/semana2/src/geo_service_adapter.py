from typing import Any
from src.old_geo_service import OldGeoService
from src.new_geo_provider import NewGeoProvider


class GeoServiceAdapter(OldGeoService):
    """
    Adaptador de Objetos (GoF): Adapta la interfaz incompatible de NewGeoProvider
    al protocolo esperado por el sistema (OldGeoService).

    Extensibilidad (¿Qué cambia si llega un 3er proveedor mañana?):
    Los 40 archivos cliente permanecen 100% inalterados. Solo se requeriría:
    1. Reemplazo directo: Modificar este adaptador para componer al nuevo servicio
       y adaptar la traducción en get_location().
    2. Open/Closed: Crear un nuevo adaptador (ej. FutureGeoAdapter) y cambiar
       únicamente la instanciación en el archivo de configuración (main.py).
    """

    def __init__(self, provider: NewGeoProvider | None = None) -> None:
        super().__init__()
        # Composición: encapsula la instancia del servicio de terceros.
        self._provider = provider if provider is not None else NewGeoProvider()

    def get_location(self, ip: str) -> dict[str, Any]:
        """
        Misma firma que el sistema espera.
        Delega la consulta al nuevo proveedor y traduce su respuesta de objetos anidados
        hacia el formato de diccionario plano que consumen los 40 archivos cliente.
        """
        resultado = self._provider.locate(ip) # Acá se delega

        # Traducción y normalización estructural de datos (gracias al nuevo proveedor)
        return {
            "lat": resultado.coordinates.latitude,
            "lng": resultado.coordinates.longitude,
            "city": resultado.address.locality,
            "country": resultado.address.nation,
        }
