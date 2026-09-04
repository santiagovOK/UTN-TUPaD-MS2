# Resolución Unidad 2 - Semana 2: Adapter - Estructura en Python


## Justificación

El sistema cuenta con más de 40 archivos clientes acoplados a la interfaz de `OldGeoService`, mientras que `NewGeoProvider` presenta una API incompatible y no modificable. Una refactorización masiva del cliente implicaría un riesgo y costo inasumibles, además de violar el principio Open/Closed. Patrones como *Facade* no aplican aquí, dado que buscan simplificar un subsistema complejo y no adaptar una interfaz preexistente específica.

El patrón **Adapter** es la solución adecuada, ya que introduce una capa intermedia que implementa la interfaz esperada por el cliente (`get_location`) y traduce la invocación hacia el nuevo proveedor (`locate`). Esto permite integrar el nuevo servicio de manera transparente sin alterar los 40 archivos existentes ni modificar el código de terceros.

**Nota sobre diseño idiomático y "Java-ismos" (Guía de cátedra):**
Aunque en Python idiomático se evitarían ciertos patrones heredados de Java, se conservaron conscientemente por las restricciones del trabajo:
1. **Herencia formal vs. Duck Typing:** Se mantuvo `GeoServiceAdapter(OldGeoService)` para reflejar el diagrama UML de GoF, aun cuando en Python el *duck typing* o un `Protocol` harían innecesaria la herencia.
2. **Prefijo `get_`:** Proviene del código *legacy/heredado* preexistente; el Adapter existe justamente para convivir con esa firma sin romper los 40 archivos cliente.
3. **Un archivo por clase:** Se mantuvieron clases separadas en `src/` para evidenciar físicamente la restricción de *"un único archivo nuevo añadido"*, en lugar de consolidar el dominio en un único módulo Python.

*Aclaración sobre `NewGeoProvider`: Al simular el proveedor de terceros (código que es cerrado y permanece inalterado), se utilizó `@dataclass` de la biblioteca estándar como la herramienta nativa adecuada para modelar sus objetos de respuesta con atributos directos, respetando estrictamente la estructura exigida en la consigna sin modificar su contrato.*

## Roles GoF y Variante de Implementación

### 1. Mapeo de Roles según la Teoría de GoF

| Rol GoF | Componente en el Proyecto | Responsabilidad en la Solución |
| :--- | :--- | :--- |
| **Cliente (*Client*)** | `src/client.py` (`run_business_logic`) | Representa los 40 archivos de lógica de negocio que consumen el servicio de geolocalización. |
| **Interfaz / Objetivo (*Target*)** | `src/old_geo_service.py` (`OldGeoService`) | Define el contrato y protocolo que el cliente sabe utilizar (`get_location(ip) -> dict`). |
| **Servicio Incompatible (*Adaptee*)** | `src/new_geo_provider.py` (`NewGeoProvider`) | Proveedor de terceros que posee la funcionalidad requerida pero con una interfaz incompatible (`locate(ip) -> LocationResponse`). |
| **Adaptador (*Adapter*)** | `src/geo_service_adapter.py` (`GeoServiceAdapter`) | Conecta ambos mundos: hereda de *Target* para cumplir el contrato del cliente y envuelve a *Adaptee* para traducir sus llamadas y estructuras de datos. |

### 2. Variante de Implementación: Adaptador de Objetos

La teoría de GoF distingue dos variantes para este patrón:
- **Clase Adaptadora (Herencia Múltiple):** El adaptador hereda de *Target* y de *Adaptee* simultáneamente. Aunque Python soporta herencia múltiple, esta variante acopla rígidamente el adaptador a la implementación concreta del proveedor de terceros en tiempo de definición.
- **Adaptador de Objetos (Composición):** Se adoptó esta variante. El adaptador implementa la interfaz esperada y compone una instancia de `NewGeoProvider` en su atributo `#_provider`. Esto respeta el principio central de GoF: *"Favorecer la composición de objetos por sobre la herencia de clases"*, permitiendo sustituir o extender el proveedor con mínimo acoplamiento.


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
3. **Transparencia verificable:** Al dejar `src/client.py` intacto, demuestra empíricamente que los 40 archivos de negocio no requieren modificación alguna para operar con el nuevo proveedor.
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

> **Nota sobre el contraste (transparencia):** Como se evidencia en el bloque anterior, el código cliente (`run_business_logic`, representativo de los 40 archivos) no sufre ningún cambio. Sigue interactuando contra la interfaz esperada (`get_location(ip)`) y recibiendo la estructura de datos habitual (`dict` con `lat`, `lng`, `city`, `country`), validando el principio Open/Closed.

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
        resultado = self._provider.locate(ip) # Acá se delega

        # Traducción y normalización estructural de datos (gracias al nuevo proveedor)
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

---

## Restricciones

Se respetaron rigurosamente todas las restricciones operativas y arquitectónicas impuestas en la consigna:

1. **Sin librerías externas:** La solución se implementó utilizando exclusivamente características nativas de Python (`typing` y `dataclasses` de la biblioteca estándar). No se instalaron ni utilizaron paquetes de terceros.
2. **Un único archivo nuevo:** La resolución del patrón se encapsuló íntegramente en un solo archivo nuevo: `src/geo_service_adapter.py`.
3. **Firma pública inalterada:** El método `get_location(self, ip: str) -> dict[str, Any]` conserva con total exactitud el nombre, los parámetros y el tipo de estructura de retorno esperados por el cliente.
4. **Código existente cerrado a modificaciones:** Ni `OldGeoService` ni `NewGeoProvider` sufrieron cambios en su código. La lógica de negocio de los 40 archivos cliente (`src/client.py`) se mantuvo intacta. El único cambio en toda la aplicación fue la instanciación en el archivo de configuración (`main.py`).




