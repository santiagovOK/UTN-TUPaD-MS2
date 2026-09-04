# Resolución Unidad 2 - Semana 2: Adapter - Estructura en Python


## Justificación

El sistema cuenta con más de 40 archivos clientes acoplados a la interfaz de `OldGeoService`, mientras que `NewGeoProvider` presenta una API incompatible y no modificable. Una refactorización masiva del cliente implicaría un riesgo y costo inasumibles, además de violar el principio Open/Closed. Patrones como *Facade* no aplican aquí, dado que buscan simplificar un subsistema complejo y no adaptar una interfaz preexistente específica.

El patrón **Adapter** es la solución adecuada, ya que introduce una capa intermedia que implementa la interfaz esperada por el cliente (`get_location`) y traduce la invocación hacia el nuevo proveedor (`locate`). Esto permite integrar el nuevo servicio de manera transparente sin alterar los 40 archivos existentes ni modificar el código de terceros.

**Nota sobre diseño idiomático en Python:** Siguiendo los lineamientos de la guía de la cátedra de Programación 4 sobre las diferencias entre Java y Python, en Python el polimorfismo no exige herencia estricta gracias al *duck typing* (o al uso de `Protocol`). Sin embargo, se conservó la relación de herencia formal `GeoServiceAdapter(OldGeoService)` para reflejar fielmente la estructura canónica del patrón Adapter de Objetos y el diagrama de clases UML solicitado en la consigna.

Para modelar los objetos de respuesta del nuevo proveedor (`NewGeoProvider`) se aprovechan las facilidades idiomáticas de Python (`dataclasses`), exponiendo atributos directos en lugar del *boilerplate* tradicional de Java.

## Estructura de Archivos
```text
.
├── main.py                     # (Refactorizado) Punto de entrada / configuración: único lugar donde cambia la instanciación.
└── src/
    ├── old_geo_service.py      # (Queda igual) Interfaz que el sistema espera.
    ├── new_geo_provider.py     # (Queda igual) Servicio de tercero incompatible.
    ├── geo_service_adapter.py  # (Nuevo) Clase adaptadora.
    └── client.py               # (Queda igual) Simula la lógica de los 40 archivos cliente del sistema.
```

## Diagrama UML Final

**Ver diagrama:** [uml/diagrama_final.md](../uml/diagrama_final.md)

## Código refactorizado: Implementación

### 1. `main.py` (Punto de entrada y configuración)
Este es el **único archivo de todo el sistema que se refactoriza**. Se decidió ubicarlo en la raíz del proyecto como punto de entrada por las siguientes razones de diseño:

1. **Separación de responsabilidades (*Composition Root*):** Aísla el ensamblado e inyección de dependencias de la lógica de negocio pura (`src/client.py`).
2. **Fidelidad con la consigna:** Cumple con la premisa de *"un único cambio en toda la app: en un archivo de configuración o fábrica"*, permitiendo contrastar de forma nítida el "Antes" y "Después".
3. **Transparencia verificable:** Al dejar `src/client.py` 100% intacto, demuestra empíricamente que los 40 archivos de negocio no requieren modificación alguna para operar con el nuevo proveedor.
4. **Punto de ejecución:** Permite ejecutar la simulación directamente con `python main.py` y verificar la salida por consola.

#### Antes (como sería `main.py` con `OldGeoService`)
```python
# main.py - Antes de la migración
from src.old_geo_service import OldGeoService
from src.client import run_business_logic

def main() -> None:
    # Instanciación original acoplada al proveedor heredado
    geo_service = OldGeoService()
    
    # Ejecución de la lógica de negocio cliente
    run_business_logic(geo_service)

if __name__ == "__main__":
    main()
```

#### Después (con `GeoServiceAdapter`)
```python
# main.py - Después de la migración
from src.geo_service_adapter import GeoServiceAdapter
from src.client import run_business_logic

def main() -> None:
    # ÚNICO CAMBIO EN TODA LA APLICACIÓN:
    # Se reemplaza la instanciación directa por el Adapter
    geo_service = GeoServiceAdapter()
    
    # El código cliente sigue exactamente igual, sin enterarse del cambio de proveedor
    run_business_logic(geo_service)

if __name__ == "__main__":
    main()
```

> **Nota sobre el contraste:** Como se evidencia en el bloque anterior, el código cliente (`run_business_logic`, representativo de los 40 archivos) no sufre ningún cambio. Sigue interactuando contra la interfaz esperada (`get_location(ip)`) y recibiendo la estructura de datos habitual (`dict` con `lat`, `lng`, `city`, `country`), validando el principio Open/Closed.

### 2. La nueva clase adaptadora (`src/geo_service_adapter.py`)

Es el único archivo **nuevo** que se agrega a la base de código. Aplica la variante de **Adaptador de Objetos** mediante composición, envolviendo una instancia de `NewGeoProvider` y exponiendo el contrato de `OldGeoService`:

```python
# src/geo_service_adapter.py
from typing import Any
from src.old_geo_service import OldGeoService
from src.new_geo_provider import NewGeoProvider

class GeoServiceAdapter(OldGeoService):
    """
    Adaptador de Objetos (GoF): Adapta la interfaz incompatible de NewGeoProvider
    al protocolo esperado por el sistema (OldGeoService).
    """

    def __init__(self, provider: NewGeoProvider | None = None) -> None:
        super().__init__()
        # Composición: encapsula la instancia del servicio de terceros
        self._provider = provider 
        if provider is not None else NewGeoProvider()

    def get_location(self, ip: str) -> dict[str, Any]:
        """
        Misma firma que el sistema espera.
        Delega la consulta al nuevo proveedor y traduce su respuesta de objetos anidados
        hacia el formato de diccionario plano que consumen los 40 archivos cliente.
        """
        resultado = self._provider.locate(ip)

        # Traducción y normalización estructural de datos
        return {
            "lat": resultado.coordinates.latitude,
            "lng": resultado.coordinates.longitude,
            "city": resultado.address.locality,
            "country": resultado.address.nation,
        }
```

---

## Extensibilidad: ¿Qué pasa si llega un tercer proveedor mañana?

Si mañana se decide incorporar un tercer proveedor (`FutureGeoProvider` / `ThirdPartyGeo`) con una interfaz completamente distinta (por ejemplo, un método `lookup_ip(ip)` que retorna tuplas o un payload XML/GeoJSON):

1. **Transparencia absoluta en el cliente:** Ninguno de los 40 archivos cliente del sistema se modifica. El código de negocio sigue consumiendo `geo.get_location(ip)`.
2. **Dos alternativas de extensión:**
   - **Opción 1 (Reemplazo directo):** Si el tercer proveedor sustituye al actual, basta con modificar **únicamente el método `get_location` dentro de `geo_service_adapter.py`**, adaptando la llamada y el mapeo al nuevo servicio.
   - **Opción 2 (Cumplimiento estricto de Open/Closed):** Si se desea mantener ambos proveedores disponibles o configurables, se crea una nueva clase `FutureGeoAdapter(OldGeoService)` que adapte al nuevo proveedor. En el archivo de configuración (`main.py`), solo se cambia la instanciación:
     ```python
     # Cambio de proveedor en una sola línea:
     geo = FutureGeoAdapter()
     ```

Esta independencia demuestra el verdadero poder del patrón: **el riesgo de regresión en los 40 archivos del sistema es cero**, confinando todo el impacto de los cambios de infraestructura externa en la capa adaptadora.



