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

