# Requerimientos — Observer: notificaciones de stock

Este documento constituye la especificación exhaustiva y trazable de requerimientos para el refactoring del sistema de inventario aplicando el patrón **Observer** (GoF). El desglose está organizado bajo un enfoque de construcción **Bottom-Up** (desde los componentes independientes y desacoplados hacia los componentes integradores, de composición y entregables finales), sirviendo como insumo directo para la generación del tablero Kanban de desarrollo.

---

## Convenciones de diseño adoptadas

A partir de las directivas de `docs/consignas.md` y los lineamientos teóricos y de modelado en `docs/guias/` (`observer_guia.md`, `javaismos_guia.md`, `howto_uml.md`), se establecen las siguientes decisiones arquitectónicas:

1. **Contrato de notificación mediante `Protocol` (Python idiomático):**
   - Siguiendo `docs/guias/javaismos_guia.md` (Capítulo 6: *Protocol: el contrato sin el acoplamiento*), la abstracción suscriptora `StockObserver` se modela con `typing.Protocol` en lugar de una jerarquía rígida con `ABC`.
   - La firma canónica del método es:
     ```python
     def on_low_stock(self, product_id: str, quantity: int) -> None: ...
     ```
   - Justificación: `StockObserver` es un contrato de capacidades que múltiples módulos independientes implementan sin necesidad de compartir código base ni acoplarse nominalmente a una superclase.

2. **Relación estructural: Agregación (`o--`), no Composición (`*--`):**
   - Siguiendo `docs/guias/howto_uml.md` (Sección 2.3: *Agregación vs. Composición*), el notificador `InventoryManager` no crea a los observadores dentro de su constructor ni es dueño de su ciclo de vida; los recibe ya instanciados desde el exterior mediante su método `subscribe()`.
   - Por ende, en el modelo UML la relación se expresa como agregación:
     `InventoryManager "1" o-- "0..*" StockObserver : notifica a`

3. **Manejo de resiliencia y aislamiento de fallos (*Fail-Safe Loop*):**
   - El bloque `try/except Exception` debe ubicarse **estrictamente dentro del bucle de notificación** de `InventoryManager`, envolviendo cada invocación individual a `observer.on_low_stock(...)`.
   - El fallo de un observador debe ser capturado y registrado sin propagar la excepción hacia el flujo del inventario ni interrumpir las notificaciones de los observadores subsiguientes.

4. **Restricciones de concurrencia y dependencias:**
   - La ejecución de las notificaciones es estrictamente **síncrona y monohilo** (sin hilos, procesos en segundo plano ni `asyncio`).
   - Cero dependencias externas: solo módulos nativos de la biblioteca estándar de Python (`typing`, `logging`, `sys`).

---

## Requerimientos de construcción Bottom-Up

### 1. Contrato independiente (Capa base de abstracción)

- **`RF-01`: Definición de la interfaz suscriptora `StockObserver`**
  - **Descripción:** Definir el contrato estructural `StockObserver` utilizando `typing.Protocol` con el método `on_low_stock(self, product_id: str, quantity: int) -> None`.
  - **Dependencias:** Ninguna (módulo base independiente).
  - **Criterios de Aceptación:**
    - El módulo no debe importar ni referenciar a `InventoryManager` ni a ningún observador concreto.
    - Debe incluir anotaciones de tipo estáticas completas (`str`, `int`, `-> None`).

- **`RF-02`: Mapeo formal de roles según la teoría de GoF**
  - **Descripción:** Formalizar conceptualmente la correspondencia de roles del patrón:
    - *Publisher / Sujeto:* `InventoryManager`.
    - *Subscriber Interface:* `StockObserver`.
    - *Concrete Subscribers:* `EmailAlertObserver`, `AnalyticsObserver`, `ReplenishObserver`, `PushNotificationObserver`.
  - **Dependencias:** `RF-01`.
  - **Criterios de Aceptación:**
    - Documentar las responsabilidades y contratos asociados a cada rol conforme a `docs/guias/observer_guia.md`.

---

### 2. Observadores concretos (Componentes hoja independientes)

- **`RF-03`: Implementación de los observadores del dominio original**
  - **Descripción:** Implementar las tres clases suscriptoras correspondientes a los servicios previamente acoplados:
    - `EmailAlertObserver`: Implementa `on_low_stock` y simula el envío de alerta de correo ("Alerta Email: Stock bajo para {product_id} ({quantity} unidades)").
    - `AnalyticsObserver`: Implementa `on_low_stock` y registra el evento en el panel analítico ("Analytics: Evento registrado para {product_id}").
    - `ReplenishObserver`: Implementa `on_low_stock` y genera la orden de reposición automática de 100 unidades ("Reposición: Orden emitida por 100 unidades para {product_id}").
  - **Dependencias:** `RF-01`.
  - **Criterios de Aceptación:**
    - Cada observador debe implementar la firma exacta de `StockObserver`.
    - Cada observador debe poder instanciarse y ejecutarse de forma aislada sin requerir la presencia de `InventoryManager`.

- **`RF-04`: Implementación de observador de extensión (`PushNotificationObserver`)**
  - **Descripción:** Implementar un nuevo observador concreto independiente, `PushNotificationObserver`, que emita notificaciones push ante eventos de stock bajo ("Push: Notificación enviada al móvil para {product_id}").
  - **Dependencias:** `RF-01`.
  - **Criterios de Aceptación:**
    - Demostrar el principio Open/Closed: la creación de este observador se realiza en su propio módulo sin modificar ninguna línea de `InventoryManager` ni de los otros observadores.

- **`RF-05`: Implementación del observador para prueba de resiliencia (`BrokenObserver`)**
  - **Descripción:** Crear la clase `BrokenObserver` que implemente `StockObserver`, cuyo método `on_low_stock` lance intencionalmente una excepción con el mensaje exacto `"error de red simulado"`.
  - **Dependencias:** `RF-01`.
  - **Criterios de Aceptación:**
    - La excepción producida debe ser estándar (ej. `RuntimeError` o `ConnectionError`) con el mensaje especificado.
    - Debe permitir verificar en tests o ejecución que el error ocurre durante la notificación.

---

### 3. Notificador (Componente integrador del patrón)

- **`RF-06`: Desacoplamiento total de dependencias en `InventoryManager`**
  - **Descripción:** Refactorizar `InventoryManager` erradicando cualquier referencia nominal, importación, instanciación directa (`NUEVO EmailAlertService()`, etc.) o llamada a servicios concretos.
  - **Dependencias:** `RF-01`.
  - **Criterios de Aceptación:**
    - Búsqueda en el archivo de `InventoryManager` no debe arrojar menciones a `EmailAlertObserver`, `AnalyticsObserver`, `ReplenishObserver`, ni a los nombres de servicios heredados.
    - El gestor solo conoce y tipa contra el protocolo genérico `StockObserver`.

- **`RF-07`: Gestión dinámica de suscriptores (`subscribe` / `unsubscribe`)**
  - **Descripción:** Proveer en `InventoryManager` una colección interna protegida `#_observers: list[StockObserver]` y métodos públicos para registrar y remover observadores:
    - `subscribe(self, observer: StockObserver) -> None`: Añade un observador si no está presente.
    - `unsubscribe(self, observer: StockObserver) -> None`: Remueve el observador si se encuentra en la lista.
  - **Dependencias:** `RF-01`, `RF-06`.
  - **Criterios de Aceptación:**
    - El constructor inicia `#_observers` como lista vacía.
    - `subscribe` y `unsubscribe` operan de forma segura sin producir efectos secundarios ni duplicaciones indeseadas.

- **`RF-08`: Mecanismo de notificación privada (`_notify`)**
  - **Descripción:** Implementar el método protegido `#_notify(self, product_id: str, quantity: int) -> None` que itere secuencialmente sobre la lista de suscriptores invocando `observer.on_low_stock(product_id, quantity)`.
  - **Dependencias:** `RF-07`.
  - **Criterios de Aceptación:**
    - Cada observador registrado debe ser invocado exactamente una vez por cada evento de notificación.
    - La notificación es síncrona en el orden de registro.

- **`RF-09`: Aislamiento de excepciones dentro del bucle de notificación**
  - **Descripción:** Envolver cada llamada individual dentro de `_notify` en un bloque `try/except Exception`.
  - **Dependencias:** `RF-08`.
  - **Criterios de Aceptación:**
    - Si un suscriptor lanza una excepción, esta es capturada y registrada (mediante `logging.error` o impresión formateada indicando el fallo del observador).
    - La ejecución continúa inmediatamente con el siguiente observador registrado sin detener la cadena ni elevar la excepción hacia el llamador de negocio.

---

### 4. Integración del evento de negocio

- **`RF-10`: Actualización de stock con umbral de alerta (`update_stock`)**
  - **Descripción:** Implementar el método `update_stock(self, product_id: str, quantity: int) -> None` que almacene la cantidad en el diccionario de stock interno `#_stock[product_id] = quantity` y, si `quantity < 10`, invoque a `self._notify(product_id, quantity)`.
  - **Dependencias:** `RF-08`, `RF-09`.
  - **Criterios de Aceptación:**
    - Si `quantity >= 10`, el stock se actualiza pero no se dispara ninguna notificación.
    - Si `quantity < 10`, se dispara `_notify`.

- **`RF-11`: Operación de venta de producto (`sell_product`)**
  - **Descripción:** Implementar el método `sell_product(self, product_id: str, sold: int) -> None` que reste la cantidad vendida al stock existente (`#_stock[product_id] -= sold`) y, si el stock resultante es menor a 10, invoque a `self._notify(product_id, new_quantity)`.
  - **Dependencias:** `RF-10`.
  - **Criterios de Aceptación:**
    - La lógica de notificación no debe duplicarse: debe reutilizar el método `_notify` interno.
    - Control de stock insuficiente (opcional / validación defensiva para no permitir stock negativo).

---

### 5. Composición y evidencia ejecutable (Punto de entrada)

- **`RF-12`: Configuración y ensamblado en punto de entrada (`main.py`)**
  - **Descripción:** Actuar como *Composition Root*: instanciar `InventoryManager`, instanciar por separado los observadores (`EmailAlertObserver`, `AnalyticsObserver`, `BrokenObserver`, `ReplenishObserver`, `PushNotificationObserver`) y suscribirlos al gestor.
  - **Dependencias:** `RF-03`, `RF-04`, `RF-05`, `RF-07`, `RF-10`.
  - **Criterios de Aceptación:**
    - Separación explícita entre la instanciación de los componentes y la ejecución de la lógica de negocio.

- **`RF-13`: Ejecución de la prueba integral de resiliencia con observador roto**
  - **Descripción:** Ejecutar `manager.update_stock("PROD-001", 5)` con la cadena de observadores incluyendo `BrokenObserver` intercalado entre ellos.
  - **Dependencias:** `RF-05`, `RF-09`, `RF-12`.
  - **Criterios de Aceptación:**
    - Evidencia en consola:
      1. `EmailAlertObserver` ejecuta OK.
      2. `AnalyticsObserver` ejecuta OK.
      3. `BrokenObserver` lanza `"error de red simulado"`, el error es capturado y logueado.
      4. `ReplenishObserver` ejecuta OK tras el fallo.
      5. `PushNotificationObserver` ejecuta OK tras el fallo.
    - La salida demuestra empíricamente que un suscriptor fallido no corta la cadena.

- **`RF-14`: Demostración del ciclo de vida de suscripción (`unsubscribe`)**
  - **Descripción:** Invocar `manager.unsubscribe(...)` sobre un observador y emitir un nuevo cambio de stock por debajo del umbral, comprobando que el observador desuscrito ya no recibe notificaciones.
  - **Dependencias:** `RF-07`, `RF-12`.
  - **Criterios de Aceptación:**
    - El observador removido no emite mensajes en la segunda ejecución.

---

### 6. Entregables y documentación técnica (En orden de dependencia)

- **`RE-01`: Modelado UML de la situación inicial acoplada**
  - **Descripción:** Crear el diagrama de clases de la situación antes del refactoring en sintaxis Mermaid (`classDiagram`), mostrando el acoplamiento rígido (composición o dependencia directa) de `InventoryManager` hacia `EmailAlertService`, `AnalyticsDashboard` y `AutoReplenishment`.
  - **Dependencias:** Análisis del código problemático de `docs/consignas.md`.
  - **Criterios de Aceptación:**
    - Utilizar convenciones de `docs/guias/howto_uml.md`.
    - Reflejar claramente por qué el diseño original viola Open/Closed.

- **`RE-02`: Modelado UML de la solución refactorizada con Observer**
  - **Descripción:** Crear el diagrama de clases de la solución final en Mermaid, reflejando:
    - Estereotipo `<<Protocol>>` en `StockObserver`.
    - Realización estructural (`..|>`) desde los observadores hacia `StockObserver`.
    - Agregación (`o--`) con multiplicidad `1` a `0..*` desde `InventoryManager` hacia `StockObserver`.
    - Visibilidad protegida `#_` para `#_observers` y `#_notify`.
    - Inclusión de `BrokenObserver` y `PushNotificationObserver`.
  - **Dependencias:** `RF-01`, `RF-03`, `RF-04`, `RF-05`, `RF-07`, `RF-08`.
  - **Criterios de Aceptación:**
    - Cumplir estrictamente las reglas de sintaxis de `docs/guias/howto_uml.md`.

- **`RE-03`: Confección del informe técnico final (`docs/informe.md`)**
  - **Descripción:** Redactar el informe completando la plantilla estructurada existente en `docs/informe.md` respetando el orden de encabezados establecido:
    1. *Justificación:* Máximo 10 líneas explicando el acoplamiento concreto resuelto (sin teoría de libro).
    2. *Roles GoF y Variante:* Mapeo formal y justificación del uso de `Protocol` idiomático frente a `ABC`.
    3. *Estructura de Archivos:* Árbol del proyecto y responsabilidades.
    4. *Diagramas UML:* Inclusión y explicación de los diagramas de `RE-01` y `RE-02`.
    5. *Código Antes vs. Después:* Contraste nítido de la refactorización.
    6. *Prueba de Resiliencia:* Evidencia y explicación del bloque `try/except` interno con `BrokenObserver`.
    7. *Extensibilidad:* Explicación de cómo `PushNotificationObserver` cumple Open/Closed.
    8. *Restricciones:* Checklist de cumplimiento normativo.
  - **Dependencias:** `RF-01` a `RF-14`, `RE-01`, `RE-02`.
  - **Criterios de Aceptación:**
    - Completar este requerimiento únicamente tras haber obtenido y verificado toda la evidencia ejecutable.
    - La justificación no debe exceder las 10 líneas estipuladas.

- **`RE-04`: Evidencia ejecutable empírica (Salidas de ejecución)**
  - **Descripción:** Capturar las trazas de ejecución completas de la consola que acrediten la resiliencia ante fallos y la extensibilidad, listas para ser citadas en el informe.
  - **Dependencias:** `RF-13`, `RF-14`.
  - **Criterios de Aceptación:**
    - Las trazas deben ser reales, no simuladas ni redactadas a mano.

---

## Restricciones y criterios de aceptación globales

| Restricción / Condicionante | Origen | Criterio de Verificación |
| :--- | :--- | :--- |
| **Sin librerías externas** | `docs/consignas.md` | El proyecto corre con Python 3 estándar puro; no existen `requirements.txt`, `poetry.lock` ni dependencias fuera de la stdlib. |
| **Notificación monohilo / síncrona** | `docs/consignas.md` | No se utilizan `threading`, `multiprocessing`, `concurrent.futures` ni `async/await`. Todo ocurre en el mismo hilo de ejecución. |
| **Desacoplamiento del notificador** | `docs/consignas.md` | `InventoryManager` no contiene nombres de observadores concretos ni importa sus módulos. |
| **Suscripción dinámica** | `docs/consignas.md` | Métodos `subscribe` y `unsubscribe` operando sobre `StockObserver`. |
| **Aislamiento de fallos** | `docs/consignas.md` | El manejo de errores está ubicado DENTRO del bucle de notificación de forma individual por suscriptor. |
| **Test del observador roto obligatorio** | `docs/consignas.md` | El código ejecuta `BrokenObserver` arrojando `"error de red simulado"` y verifica la continuidad del bucle. |
| **Nuevo observador (Open/Closed)** | `docs/consignas.md` | Se agrega `PushNotificationObserver` sin modificar una sola línea de `InventoryManager`. |
| **Diagramas UML Antes y Después** | `docs/consignas.md` / `guias/` | Diagramas en Mermaid que reflejan la situación inicial y refactorizada con sintaxis Python-UML. |
| **Justificación de máximo 10 líneas** | `docs/consignas.md` | Explicación concreta del problema de acoplamiento resuelto sin definiciones enciclopédicas. |
| **Justificación de variantes de diseño** | `docs/consignas.md` / `guias/` | Explicitar en el informe la adopción de `Protocol` (tipado estructural sin herencia obligatoria) y Agregación (`o--`). |

---

## Matriz de trazabilidad de la consigna

La siguiente matriz vincula cada párrafo y exigencia de `docs/consignas.md` con los identificadores de requerimiento de este documento:

| Exigencia en `docs/consignas.md` | Sección / Líneas | Requerimiento(s) Asociado(s) |
| :--- | :--- | :--- |
| Acoplamiento original en `InventoryManager` con 3 servicios concretos | Líneas 36–73 | `RF-06`, `RE-01` |
| Lista genérica de suscriptores e interfaz común `onLowStock` | Líneas 79–95, 103–108 | `RF-01`, `RF-02`, `RF-07` |
| Servicios que implementan la interfaz suscriptora | Líneas 109–128 | `RF-03` |
| Métodos `subscribe`, `unsubscribe` y `notify` en el gestor | Líneas 129–166 | `RF-07`, `RF-08`, `RF-10`, `RF-11` |
| Manejo de errores DENTRO del bucle para no cortar la cadena | Líneas 153–158, 167–168 | `RF-09` |
| Observador roto con excepción de error simulado | Líneas 174–195 | `RF-05`, `RF-13` |
| Extensibilidad con nuevo observador sin tocar el manager | Líneas 196–201 | `RF-04`, `RF-12` |
| Restricción: notificaciones síncronas y sin librerías | Líneas 202–204, 223–226 | `Convenciones`, `RF-08`, Restricciones globales |
| Entrega: Diagramas UML Antes y Después | Líneas 211–213 | `RE-01`, `RE-02` |
| Entrega: Contraste Antes vs. Después | Líneas 214 | `RE-04` |
| Entrega: Justificación concisa en máximo 10 líneas | Líneas 215 | `RE-03` |
| Entrega: Justificar desviaciones o particularidades del lenguaje | Líneas 231–232 | `Convenciones`, `RE-03` |
