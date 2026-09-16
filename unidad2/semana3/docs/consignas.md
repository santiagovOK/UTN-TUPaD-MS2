Patrones de Diseño GoF — Trabajo Práctico · 3 de 3&nbsp;

*Categoría GoF: Comportamiento (Behavioral)*&nbsp;

**Observer**&nbsp;

*Refactoring en el mundo real — Sistema de inventario que notifica a múltiples servicios*&nbsp;

| Parámetro&nbsp; | Valor |
| :---- | :---- |
| **Asignatura**&nbsp; | Metodologia de Sistemas II |
| **Modalidad**&nbsp; | Trabajo Práctico Individual |
| **Tiempo estimado**&nbsp; | 2 a 3 horas |
| **Lenguaje**&nbsp; | Java, Python, C\# o TypeScript |
| **Restricción**&nbsp; | Sin librerías externas |

&nbsp;

&nbsp;

**¿De qué trata este trabajo?**&nbsp;

Esto no es un ejercicio teórico sobre definiciones. Es una simulación de lo que pasa todos los  días en proyectos que llevan tiempo vivos: código que funciona, pero que ya nadie quiere tocar.  Vas a recibir código real con problemas reales, y tu trabajo es entrar, entender qué está  fallando, y refactorizarlo aplicando el patrón Observer.&nbsp;

Si entendés bien este patrón, tenés la lógica base para abordar cualquier patrón de  comportamiento de la familia GoF por tu cuenta.&nbsp;

| Restricción global  No uses librerías externas. Todo se resuelve con el lenguaje base que elijas. El objetivo es  demostrar que entendés el patrón, no que encontraste una librería que lo implementa. |
| :---- |

&nbsp;

&nbsp;

**¿Qué está pasando en el proyecto?**&nbsp;

Tenemos un sistema de inventario. Cada vez que el stock de un producto baja, hay que  notificar a tres sistemas: alertas por email, el panel de analytics y el módulo de reposición  automática. El developer original lo hizo directo. Muy directo.&nbsp;

**El código problemático**&nbsp;

CLASE InventoryManager:&nbsp;

&nbsp;CONSTRUCTOR:&nbsp;

&nbsp;this.emailService \= NUEVO EmailAlertService()&nbsp;

&nbsp;this.analytics \= NUEVO AnalyticsDashboard()&nbsp;

&nbsp;this.replenishment \= NUEVO AutoReplenishment()

&nbsp;MÉTODO update\_stock(productId, quantity):&nbsp;

&nbsp;this.stock\[productId\] \= quantity&nbsp;

&nbsp;SI quantity \< 10:&nbsp;

&nbsp;this.emailService.send\_low\_stock\_alert(productId, quantity)  this.analytics.record\_low\_stock\_event(productId)&nbsp;

&nbsp;this.replenishment.trigger\_order(productId, 100\)&nbsp;

&nbsp;MÉTODO sell\_product(productId, sold):&nbsp;

&nbsp;this.stock\[productId\] \-= sold&nbsp;

&nbsp;SI this.stock\[productId\] \< 10:&nbsp;

&nbsp;this.emailService.send\_low\_stock\_alert(productId, ...)&nbsp;

&nbsp;this.analytics.record\_low\_stock\_event(productId)&nbsp;

&nbsp;this.replenishment.trigger\_order(productId, 100\)&nbsp;

| El problema de fondo  El InventoryManager conoce por nombre a EmailAlertService, AnalyticsDashboard y  AutoReplenishment. Si cualquiera de los tres cambia, o si querés agregar notificaciones  push, tenés que abrir el InventoryManager. Que no tiene nada que ver con emails ni con  analytics. Eso es acoplamiento. |
| :---- |

&nbsp;

&nbsp;

**¿Qué hace el patrón Observer?**&nbsp;

El InventoryManager mantiene una lista genérica de "cosas que quieren saber cuando algo  cambia". Cuando el stock baja, recorre la lista y avisa a cada uno. No sabe quiénes son — solo  sabe que tienen un método onLowStock(). Cada observador decide qué hacer con el aviso.&nbsp;

**Anclaje teórico**&nbsp;

Observer (también llamado Observador, Publicación-Suscripción, Event-Subscriber, Listener)  es un patrón de diseño de comportamiento que define un mecanismo de suscripción para  notificar a varios objetos sobre cualquier evento que le suceda al objeto que están observando.&nbsp;

La estructura canónica del patrón identifica tres roles principales:&nbsp;

• **Notificador (Publisher):** Envía eventos de interés a otros objetos. Mantiene el campo  de suscriptores y los métodos subscribe/unsubscribe/notifySubscribers.&nbsp;

• **Interfaz Suscriptora:** Declara la interfaz de notificación. Consiste típicamente en un  único método update con parámetros de contexto.&nbsp;

• **Suscriptores Concretos:** Realizan acciones en respuesta a las notificaciones.  Implementan la misma interfaz para que el notificador no esté acoplado a clases  concretas.&nbsp;

En este ejercicio, InventoryManager juega el rol de Notificador, StockObserver es la Interfaz  Suscriptora, y EmailAlertObserver/AnalyticsObserver/ReplenishObserver son los Suscriptores  Concretos.&nbsp;

**Diagrama UML — Antes vs Después**&nbsp;

(Incluí en tu entrega un diagrama UML de la situación inicial y otro de la solución refactorizada.)

**Pseudocódigo de la solución**&nbsp;

**1\. La interfaz del observador**&nbsp;

INTERFAZ StockObserver:&nbsp;

&nbsp;MÉTODO onLowStock(productId, quantity)&nbsp;

**2\. Cada servicio implementa la interfaz**&nbsp;

CLASE EmailAlertObserver IMPLEMENTA StockObserver:&nbsp;

&nbsp;MÉTODO onLowStock(productId, qty):&nbsp;

&nbsp;enviar email "Stock bajo: " \+ productId&nbsp;

CLASE AnalyticsObserver IMPLEMENTA StockObserver:&nbsp;

&nbsp;MÉTODO onLowStock(productId, qty):&nbsp;

&nbsp;registrar evento en el dashboard&nbsp;

CLASE ReplenishObserver IMPLEMENTA StockObserver:&nbsp;

&nbsp;MÉTODO onLowStock(productId, qty):&nbsp;

&nbsp;crear orden de reposición por 100 unidades&nbsp;

**3\. El manager solo conoce la interfaz**&nbsp;

CLASE InventoryManager:&nbsp;

&nbsp;CONSTRUCTOR:&nbsp;

&nbsp;this.observers \= \[\] // lista vacía, sin nombres concretos&nbsp;

&nbsp;MÉTODO subscribe(observer: StockObserver):&nbsp;

&nbsp;this.observers.agregar(observer)&nbsp;

&nbsp;MÉTODO unsubscribe(observer: StockObserver):&nbsp;

&nbsp;this.observers.remover(observer)&nbsp;

&nbsp;MÉTODO notify(productId, qty): // privado&nbsp;

&nbsp;PARA CADA observer EN this.observers:&nbsp;

&nbsp;INTENTAR:&nbsp;

&nbsp;observer.onLowStock(productId, qty)&nbsp;

&nbsp;SI FALLA: // DENTRO del loop&nbsp;

&nbsp;registrar el error&nbsp;

&nbsp;CONTINUAR con el siguiente // no detiene la cadena&nbsp;

&nbsp;MÉTODO update\_stock(productId, qty):&nbsp;

&nbsp;this.stock\[productId\] \= qty&nbsp;

&nbsp;SI qty \< 10:&nbsp;

&nbsp;this.notify(productId, qty)

| Truco clave — dónde va el manejo de errores  El bloque de captura de errores debe estar DENTRO del loop, envolviendo cada llamada  individual. Si está FUERA: el primer observer que falla corta toda la cadena. Si está  DENTRO: cada observer es independiente — uno puede fallar sin afectar a los demás. |
| :---- |

&nbsp;

&nbsp;

**4\. Código de prueba — el observer que falla**&nbsp;

manager \= NUEVO InventoryManager()&nbsp;

manager.subscribe(NUEVO EmailAlertObserver())&nbsp;

manager.subscribe(NUEVO AnalyticsObserver())&nbsp;

CLASE ObservadorRoto IMPLEMENTA StockObserver:&nbsp;

&nbsp;MÉTODO onLowStock(productId, qty):&nbsp;

&nbsp;LANZAR excepción "error de red simulado"&nbsp;

manager.subscribe(NUEVO ObservadorRoto())&nbsp;

manager.subscribe(NUEVO ReplenishObserver())&nbsp;

// Resultado esperado:&nbsp;

// email OK | ObservadorRoto falla y se registra | replenish OK manager.update\_stock("PROD-001", 5\)&nbsp;

**Tu misión**&nbsp;

• Refactorizá el InventoryManager con Observer.&nbsp;

• El manager no puede referenciar a ningún observador concreto por nombre. • Demostrá en código que un observer que falla no detiene a los demás. • Agregá un observador nuevo (puede ser push, SMS, lo que quieras) para demostrar  que el sistema es extensible sin tocar el manager.&nbsp;

| Restricciones  Sin threads ni procesos adicionales — las notificaciones son síncronas. El test del observer  roto es obligatorio en la entrega. |
| :---- |

&nbsp;

&nbsp;

**¿Qué espero ver en tu entrega?**

| Qué evalúo&nbsp; | Lo que estoy mirando |
| :---- | :---- |
| **Diagrama UML**&nbsp; | Antes y después. No tiene que ser perfecto — tiene que  contar la historia a la primera. |
| **Antes / Después**&nbsp; | El código original junto al refactorizado. Sin el contraste no  sé si entendiste qué estaba mal. |
| **Justificación**&nbsp; | Máximo 10 líneas explicando qué problema específico  resolvió el patrón en este ejercicio. No la definición del libro. |
| **Legibilidad**&nbsp; | El código refactorizado debe entenderse sin explicaciones. |
| **Test del observer roto**&nbsp; | El observer que explota y los demás siguen corriendo. Tiene  que estar en el código — no alcanza con mencionarlo. |

&nbsp;

&nbsp;

| Qué evalúo&nbsp; | Lo que estoy mirando |
| :---- | :---- |
| **Restricciones**&nbsp; | Todas respetadas. Librería externa \= ejercicio no cuenta,  aunque el código sea brillante. |

&nbsp;

&nbsp;

| Última cosa  Si tu solución no encaja del todo con el patrón "canónico" del libro, explicá por qué la  elegiste así. Eso me dice más sobre cómo pensás que si copiaste la implementación de un  tutorial. |
| :---- |

&nbsp;

&nbsp;