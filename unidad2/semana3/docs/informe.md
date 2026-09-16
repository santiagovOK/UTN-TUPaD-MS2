# Resolución Unidad 2 - Semana 3: Observer - Estructura en Python

## Justificación

## Roles GoF y Variante de Implementación

### 1. Mapeo de Roles según la Teoría de GoF

### 2. Variante de Implementación: Observador por Suscripción

## Estructura de Archivos
```text
.
├── main.py                             # (Refactorizado) Punto de entrada y Composition Root: ensambla observadores y ejecuta la simulación integral.
├── docs/
│   ├── consignas.md                    # (Queda igual) Enunciado original y restricciones del trabajo práctico.
│   ├── requerimientos.md               
│   ├── informe.md                      # (Modificado) Documento técnico de entrega con justificación, UML y evidencias.
│   └── guias/                          
└── src/
    ├── stock_observer.py               # (Nuevo) Interfaz/Protocolo suscriptor base (on_low_stock).
    ├── inventory_manager.py            # (Modificado / Refactorizado) Sujeto/Notificador: desacoplado de clases concretas, con gestión dinámica y bucle resiliente.
    ├── email_alert_observer.py         # (Refactorizado) Suscriptor concreto de alertas por email (reemplaza al acoplamiento directo de EmailAlertService).
    ├── analytics_observer.py           # (Refactorizado) Suscriptor concreto de métricas (reemplaza al acoplamiento directo de AnalyticsDashboard).
    ├── replenish_observer.py           # (Refactorizado) Suscriptor concreto de reposición automática (reemplaza al acoplamiento directo de AutoReplenishment).
    ├── push_notification_observer.py   # (Nuevo) Suscriptor de extensión para demostrar principio Open/Closed sin tocar el gestor.
    └── broken_observer.py              # (Nuevo) Suscriptor de prueba con fallo simulado para validar resiliencia del bucle de notificación.
```

### Impacto de la refactorización en los componentes:

1. **Archivos nuevos (`Nuevo`):**
   - `src/stock_observer.py`: Define el contrato abstracto (`typing.Protocol`) con el método `on_low_stock(product_id, quantity)`. No existía en el diseño original y es el elemento clave que rompe el acoplamiento.
   - `src/push_notification_observer.py`: Suscriptor adicional creado para demostrar el principio Open/Closed (permite agregar nuevos canales sin alterar `InventoryManager`).
   - `src/broken_observer.py`: Suscriptor de prueba con excepción intencional (`"error de red simulado"`) para verificar el aislamiento de fallos dentro del bucle de notificación.

2. **Archivos modificados / refactorizados (`Modificado` / `Refactorizado`):**
   - `src/inventory_manager.py`: Pasa de instanciar e invocar rígidamente a los 3 servicios concretos en su constructor y métodos a gestionar una colección polimórfica `#_observers: list[StockObserver]`, incorporando `subscribe()`, `unsubscribe()` y `_notify()` con manejo de excepciones por observador.
   - `src/email_alert_observer.py`: Adapta el servicio de alertas por correo original (`EmailAlertService`) para implementar el método estándar `on_low_stock`.
   - `src/analytics_observer.py`: Adapta el panel analítico original (`AnalyticsDashboard`) para responder al evento uniforme de notificación.
   - `src/replenish_observer.py`: Adapta el módulo de reposición automática (`AutoReplenishment`) para desacoplar su invocación del gestor de stock.
   - `main.py`: Se reestructura como *Composition Root*, desacoplando la instanciación de dependencias de la lógica de negocio y ejecutando las pruebas de resiliencia y extensibilidad.

3. **Archivos que quedan igual (`Queda igual`):**
   - Documentación de consignas y guías teóricas de consulta (`docs/consignas.md`, `docs/requerimientos.md`, `docs/guias/`).

## Diagramas UML

### 1. Situación inicial: `InventoryManager` acoplado

### 2. Solución refactorizada: Observer

## Código: Situación Inicial

### `InventoryManager` con dependencias concretas

## Código Refactorizado: Implementación

### 1. Interfaz `StockObserver`

### 2. Observadores concretos

### 3. `InventoryManager` como notificador

### 4. Configuración y ejecución

## Prueba de resiliencia: observador que falla

## Extensibilidad: nuevo observador sin modificar el manager

## Restricciones
