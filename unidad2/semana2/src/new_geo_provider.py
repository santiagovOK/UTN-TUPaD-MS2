from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinates:
    latitude: float
    longitude: float


@dataclass(frozen=True)
class Address:
    locality: str
    nation: str


@dataclass(frozen=True)
class LocationResponse:
    coordinates: Coordinates
    address: Address


class NewGeoProvider:
    """
    Nuevo proveedor de geolocalización (Adaptee / Servicio de terceros).
    Su API es completamente incompatible con OldGeoService y no puede modificarse.
    """

    def locate(self, ip: str) -> LocationResponse:
        """
        Retorna la información estructurada en objetos anidados con nombres de atributos distintos.
        """
        return LocationResponse(
            coordinates=Coordinates(
                latitude=-34.6037,
                longitude=-58.3816,
            ),
            address=Address(
                locality="Buenos Aires",
                nation="Argentina",
            ),
        )
