# Resolución Unidad 2 - Semana 3: Observer - Estructura en Python

## Justificación

## Roles GoF y Variante de Implementación

### 1. Mapeo de Roles según la Teoría de GoF

La estructura canónica del patrón identifica tres roles principales según se detalla en `docs/consignas.md`:

| Rol GoF | Componente en el Proyecto | Responsabilidad en la Solución |
| :--- | :--- | :--- |
| **Notificador** | `src/inventory_manager.py` (`InventoryManager`) | Envía eventos de interés a otros objetos. Mantiene el campo de suscriptores (`#_observers`) y los métodos `subscribe`, `unsubscribe` y `_notify`. En este ejercicio, juega el rol de Notificador. |
| **Interfaz Suscriptora** | `src/stock_observer.py` (`StockObserver`) | Declara la interfaz de notificación común con el método `on_low_stock(product_id: str, quantity: int) -> None`. |
| **Suscriptores Concretos** | `EmailAlertObserver`, `AnalyticsObserver`, `ReplenishObserver` | Realizan acciones en respuesta a las notificaciones (`on_low_stock`), implementando la misma interfaz para que el notificador no esté acoplado a clases concretas. |

### 2. Variante de Implementación: Observador por Suscripción

La teoría tradicional de GoF propone típicamente una interfaz nominal o clase abstracta (`ABC` con `@abstractmethod` en el caso de Python) que obliga a las subclases a heredar explícitamente.

En este proyecto se adoptó la variante de **Tipado Estructural mediante `typing.Protocol`** (Python idiomático), conforme a los lineamientos de `docs/guias/javaismos_guia.md` (Capítulo 6: *Protocol: el contrato sin el acoplamiento*):

1. **Contrato sin acoplamiento de herencia:** Cualquier clase que implemente el método `on_low_stock(self, product_id: str, quantity: int) -> None` satisface el protocolo automáticamente (*duck typing* verificable estáticamente), sin necesidad de acoplarse nominalmente a una superclase compartida ni cargar peso muerto en la jerarquía.
2. **Modelo de Agregación:** Siguiendo `docs/guias/howto_uml.md`, la relación entre `InventoryManager` y los observadores es de **Agregación (`o--`)**, ya que los suscriptores se crean externamente y se registran dinámicamente mediante `subscribe()`, preservando ciclos de vida independientes.
3. **Manejo de errores dentro del bucle:** La notificación se procesa de forma síncrona en un único hilo, pero encapsulando cada llamada en un bloque `try/except Exception` individual dentro del bucle. Esto garantiza que un observador defectuoso no detenga la notificación del resto.

## Estructura de Archivos
> **Aclaración sobre organización y java-ismos:** La refactorización se presenta en varios archivos `.py`, aproximadamente uno por componente del patrón. En Python no es idiomático separar cada clase en su propio módulo. Un archivo puede agrupar las clases que tengan sentido cohesivo. Se conserva conscientemente esta organización por fidelidad a la consigna y para hacer visibles, con claridad, los roles y las colaboraciones del patrón Observer. No representa una recomendación general de estructura para proyectos Python.

```text
.
├── main.py                             # (Refactorizado) Punto de entrada y código de prueba: ensambla observadores y ejecuta la simulación integral.
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
    ├── push_notification_observer.py   # (Nuevo) Suscriptor de extensión para demostrar que el sistema es extensible sin tocar el manager.
    └── broken_observer.py              # (Nuevo) Suscriptor de prueba con fallo simulado para validar resiliencia del bucle de notificación.
```

### Impacto de la refactorización en los componentes:

1. **Archivos nuevos (`Nuevo`):**
   - `src/stock_observer.py`: Define el contrato abstracto (`typing.Protocol`) con el método `on_low_stock(product_id, quantity)`. No existía en el diseño original y es el elemento clave que rompe el acoplamiento.
   - `src/push_notification_observer.py`: Suscriptor adicional creado para demostrar que el sistema es extensible sin tocar el manager (permite agregar nuevos canales sin alterar `InventoryManager`).
   - `src/broken_observer.py`: Suscriptor de prueba con excepción intencional (`"error de red simulado"`) para verificar el aislamiento de fallos dentro del bucle de notificación.

2. **Archivos modificados / refactorizados (`Modificado` / `Refactorizado`):**
   - `src/inventory_manager.py`: Pasa de instanciar e invocar rígidamente a los 3 servicios concretos en su constructor y métodos a gestionar una colección polimórfica `#_observers: list[StockObserver]`, incorporando `subscribe()`, `unsubscribe()` y `_notify()` con manejo de excepciones por observador.
   - `src/email_alert_observer.py`: Adapta el servicio de alertas por correo original (`EmailAlertService`) para implementar el método estándar `on_low_stock`.
   - `src/analytics_observer.py`: Adapta el panel analítico original (`AnalyticsDashboard`) para responder al evento uniforme de notificación.
   - `src/replenish_observer.py`: Adapta el módulo de reposición automática (`AutoReplenishment`) para desacoplar su invocación del gestor de stock.
   - `main.py`: Se reestructura como código de prueba, configurando y suscribiendo los observadores para ejecutar las pruebas de resiliencia y extensibilidad.

## Diagramas UML

### 1. Situación inicial: `InventoryManager` acoplado
**Ver diagrama:** [uml/diagrama_inicial.md](../uml/diagrama_inicial.md)

El estado inicial concentra en `InventoryManager` la creación y el uso directo de `EmailAlertService`, `AnalyticsDashboard` y `AutoReplenishment`. Cada relación es una composición: incorporar o cambiar un canal de notificación obliga a editar el gestor, que es precisamente el acoplamiento que resolverá Observer.


### 2. Solución refactorizada: Observer

## Código: Situación Inicial

### `InventoryManager` con dependencias concretas

El diseño inicial acoplaba directamente el gestor de inventario con las implementaciones específicas de los servicios de notificación:

```python
# Situación inicial problemática: dependencias rígidas en InventoryManager
class InventoryManager:
    def __init__(self) -> None:
        # Acoplamiento directo a servicios concretos
        self.email_service = EmailAlertService()
        self.analytics = AnalyticsDashboard()
        self.replenishment = AutoReplenishment()
        self.stock: dict[str, int] = {}

    def update_stock(self, product_id: str, quantity: int) -> None:
        self.stock[product_id] = quantity
        if quantity < 10:
            # Invocación directa a cada servicio concreto
            self.email_service.send_low_stock_alert(product_id, quantity)
            self.analytics.record_low_stock_event(product_id)
            self.replenishment.trigger_order(product_id, 100)

    def sell_product(self, product_id: str, sold: int) -> None:
        self.stock[product_id] -= sold
        if self.stock[product_id] < 10:
            # Duplicación de lógica y dependencias rígidas
            self.email_service.send_low_stock_alert(product_id, self.stock[product_id])
            self.analytics.record_low_stock_event(product_id)
            self.replenishment.trigger_order(product_id, 100)
```

## Código Refactorizado: Implementación

### 1. Interfaz `StockObserver`

Contrato estructural definido mediante `typing.Protocol` que desacopla el notificador de los observadores concretos:

```python
# src/stock_observer.py
from typing import Protocol


class StockObserver(Protocol):
    """
    Protocolo estructural que define la interfaz suscriptora común (GoF).
    Cualquier observador debe implementar este método para recibir notificaciones
    de eventos de stock bajo.
    """

    def on_low_stock(self, product_id: str, quantity: int) -> None:
        """
        Método de notificación invocado cuando el stock de un producto cae por debajo del umbral.

        :param product_id: Identificador del producto.
        :param quantity: Cantidad actual de stock restante.
        """
        ...
```

### 2. Observadores concretos

Cada servicio implementa el método `on_low_stock` satisfaciendo el protocolo `StockObserver` de forma puramente estructural (sin necesidad de importar ni heredar explícitamente de `StockObserver`, eliminando el acoplamiento nominal):
```python
# src/email_alert_observer.py
class EmailAlertObserver:
    """
    Suscriptor concreto de alertas por email.
    Implementa el protocolo StockObserver.
    """

    def on_low_stock(self, product_id: str, quantity: int) -> None:
        print(f"Alerta Email: Stock bajo para {product_id} ({quantity} unidades)")
```

```python
# src/analytics_observer.py
class AnalyticsObserver:
    """
    Suscriptor concreto de métricas y analítica.
    Implementa el protocolo StockObserver.
    """

    def on_low_stock(self, product_id: str, quantity: int) -> None:
        print(f"Analytics: Evento registrado para {product_id}")
```

```python
# src/replenish_observer.py
class ReplenishObserver:
    """
    Suscriptor concreto de reposición automática.
    Implementa el protocolo StockObserver.
    """

    def on_low_stock(self, product_id: str, quantity: int) -> None:
        print(f"Reposición: Orden emitida por 100 unidades para {product_id}")
```

```python
# src/push_notification_observer.py
class PushNotificationObserver:
    """
    Suscriptor concreto de notificaciones push.
    Demuestra que el sistema es extensible sin tocar el InventoryManager
    ni requerir herencia nominal.
    """

    def on_low_stock(self, product_id: str, quantity: int) -> None:
        print(f"Push: Notificación enviada al móvil para {product_id}")
```

```python
# src/broken_observer.py
class BrokenObserver:
    """
    Suscriptor concreto para prueba de resiliencia ante fallos.
    Lanza intencionalmente un error para comprobar que el bucle
    de notificación del notificador no se detiene.
    """

    def on_low_stock(self, product_id: str, quantity: int) -> None:
        raise RuntimeError("error de red simulado")
```
### 3. `InventoryManager` como notificador

En el diseño refactorizado ("Después"), `InventoryManager` elimina por completo las dependencias rígidas hacia clases concretas de servicios. Ya no instancia ni invoca directamente a `EmailAlertService`, `AnalyticsDashboard` o `AutoReplenishment`. En su lugar:

- Administra dinámicamente una colección de observadores a través de `subscribe()` y `unsubscribe()`, conociendo únicamente el protocolo abstracto `StockObserver`.
- Centraliza la emisión de alertas en el método privado `_notify()`, el cual envuelve cada llamada en un bloque `try/except` individual dentro del bucle para garantizar que un observador que falle no corte toda la cadena ni detenga a los demás.
- Los métodos de negocio `update_stock()` y `sell_product()` gestionan el estado del stock interno y, al cruzar el umbral crítico (`< 10`), delegan la notificación a `_notify()` sin duplicación de lógica ni acoplamiento hacia servicios específicos, demostrando que el sistema es extensible sin tocar el manager.
> **Preservación de `sell_product` y no regresión:**  
> Si bien la sección *"Pseudocódigo de la solución"* de `docs/consignas.md` solo ilustra `update_stock` para sintetizar didácticamente la mecánica del patrón, `sell_product` forma parte fundamental del código original preexistente (*"El código problemático"*, líneas 60–70). En una refactorización real de software legado no deben destruirse funcionalidades de negocio; por ende, se preserva y refactoriza para reutilizar limpiamente el método centralizado `_notify()`, eliminando las dependencias rígidas y la duplicación de código previa.

```python
# src/inventory_manager.py
import logging
from src.stock_observer import StockObserver


class InventoryManager:
    """
    Sujeto / Notificador del inventario.

    Diseño desacoplado (GoF - Observer):
    No utiliza referencia nominal, importación o instanciación directa
    de servicios concretos (EmailAlertService, AnalyticsDashboard, AutoReplenishment, etc.).
    Solo se comunica y tipa a través del protocolo genérico StockObserver.
    """

    def __init__(self) -> None:
        self._observers: list[StockObserver] = []
        self._stock: dict[str, int] = {}

    def subscribe(self, observer: StockObserver) -> None:
        """
        Registra un nuevo observador en la lista si no está previamente agregado.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: StockObserver) -> None:
        """
        Remueve un observador de la lista si se encuentra presente.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify(self, product_id: str, quantity: int) -> None:
        """
        Notifica síncronamente a todos los observadores registrados.
        Manejo de errores dentro del bucle:
        El bloque try/except envuelve cada llamada individual dentro del bucle
        para que un observador defectuoso no detenga la notificación del resto.
        """
        for observer in self._observers:
            try:
                observer.on_low_stock(product_id, quantity)
            except Exception as e:
                logging.error(f"Error notificando al observador {type(observer).__name__}: {e}")

    def update_stock(self, product_id: str, quantity: int) -> None:
        """
        Actualiza el nivel de stock de un producto.
        Si la cantidad cae por debajo del umbral crítico (< 10), dispara la notificación.
        """
        self._stock[product_id] = quantity
        if quantity < 10:
            self._notify(product_id, quantity)

    def sell_product(self, product_id: str, sold: int) -> None:
        """
        Registra la venta de unidades de un producto reduciendo su stock disponible.

        Nota de diseño y no regresión:
        Si bien este método no se reitera en el "Pseudocódigo de la solución" de las consignas, se preserva
        por tratarse de una funcionalidad de negocio preexistente del código original problemático.
        Se refactoriza para reutilizar el método centralizado _notify(), evitando duplicación
        de lógica y eliminando las dependencias rígidas anteriores.

        Evita valores negativos de stock.
        Si el stock resultante es menor a 10 unidades, notifica a los observadores.
        """
        current_stock = self._stock.get(product_id, 0)
        new_quantity = max(0, current_stock - sold)
        self._stock[product_id] = new_quantity
        if new_quantity < 10:
            self._notify(product_id, new_quantity)
```
### 4. Código de prueba — configuración y ejecución

El archivo `main.py` implementa el código de prueba requerido por la consigna ("4. Código de prueba — el observer que falla"). En este archivo se instancian los observadores concretos y se registran en `InventoryManager` mediante `subscribe()` antes de ejecutar las operaciones de actualización de stock.

## Prueba de resiliencia: observador que falla

La consigna establece como requisito mandatorio:
> *"Demostrá en código que un observer que falla no detiene a los demás. [...] El test del observer roto es obligatorio en la entrega."* (`docs/consignas.md`, líneas 200 y 202).

En `main.py`, la prueba se materializa suscribiendo un `BrokenObserver` intercalado entre los observadores estándar:
1. `EmailAlertObserver`
2. `AnalyticsObserver`
3. `BrokenObserver` (lanza `RuntimeError("error de red simulado")`)
4. `ReplenishObserver`
5. `PushNotificationObserver`

Al invocar `manager.update_stock("PROD-001", 5)`, la ejecución evidencia que:
- Los dos primeros observadores procesan la alerta exitosamente emitiendo sus correspondientes salidas.
- Al llegar al tercer observador, este arroja la excepción simulada. Gracias al manejo de errores dentro del loop envolviendo cada llamada individual en un bloque `try/except Exception` dentro de `InventoryManager._notify()`, la falla es capturada y registrada mediante `logging.error` sin propagarse hacia el invocador ni interrumpir el bucle.
- La iteración continúa inmediatamente, notificando con total normalidad a `ReplenishObserver` y `PushNotificationObserver`.

## Extensibilidad: nuevo observador sin modificar el manager

La consigna solicita:
> *"Agregá un observador nuevo (puede ser push, SMS, lo que quieras) para demostrar que el sistema es extensible sin tocar el manager."*

Para cumplir esta directiva se incorporó `PushNotificationObserver` (`src/push_notification_observer.py`):
1. **Extensibilidad sin tocar el manager:** Se incorpora un canal móvil (push) demostrando que el sistema es extensible sin tocar el `InventoryManager` ni alterar el código existente.
2. **Tipado Estructural (`typing.Protocol`):** `PushNotificationObserver` no hereda de ninguna clase base ni importa a `InventoryManager`; simplemente implementa el método `on_low_stock(self, product_id: str, quantity: int) -> None`.
3. **Gestión Dinámica (`unsubscribe`):** `main.py` demuestra además que el ciclo de vida es completamente dinámico: al llamar `manager.unsubscribe(push_obs)`, el observador deja de recibir notificaciones en eventos subsiguientes (`PROD-002`), sin reiniciar el sistema ni afectar al resto de los suscriptores.

## Restricciones

Se verificó el cumplimiento estricto de todas las restricciones estipuladas en `docs/consignas.md`:

| Restricción en Consigna | Estado | Justificación / Evidencia Técnica |
| :--- | :--- | :--- |
| **Sin librerías externas** (líneas 15, 27, 225) | **Cumplido** | Se utilizó exclusivamente la biblioteca estándar de Python (`typing.Protocol` para tipado estructural y `logging` para el registro de errores). No se requiere ningún paquete externo (`pip freeze` limpio). |
| **Sin threads ni procesos adicionales** (línea 202) | **Cumplido** | Toda la lógica de notificación es 100% síncrona y secuencial en un único hilo de ejecución, tal como solicita la consigna. |
| **El manager no conoce nombres concretos** (línea 200) | **Cumplido** | `InventoryManager` únicamente referencia el protocolo genérico `StockObserver`. No contiene mención, importación ni instanciación de servicios concretos. |
| **Test del observer roto obligatorio** (líneas 202, 217) | **Cumplido** | Integrado y ejecutable en `main.py` con `BrokenObserver`, verificando empíricamente el aislamiento de fallos en consola. |
