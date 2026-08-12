# Informe: Análisis de Violaciones SOLID - Parte A (Diagnóstico del Diseño)

## Objetivo
Este informe documenta el diagnóstico del diseño del sistema de gestión de notificaciones del Hospital Central, identificando las violaciones de los principios SOLID y describiendo el impacto en la mantenibilidad y el costo de cambio.

---

# Parte A — Diagnóstico del Diseño

## A. Indicar qué principios SOLID se están violando.

El código base, encapsulado en la clase `Notificador`, presenta al menos las siguientes violaciones:

### SRP (Single Responsibility Principle)
La clase `Notificador` viola el SRP al asumir la responsabilidad de manejar la lógica de múltiples canales de comunicación (Email, SMS, WhatsApp). Según el SRP, una clase debe tener una única razón para cambiar. Al tener múltiples tipos de notificaciones, `Notificador` es sensible a cambios en cada canal.

### OCP (Open/Closed Principle)
El diseño es cerrado a la extensión y abierto a la modificación. La implementación del método `enviar` utiliza condicionales (`if` statements) que requieren que se altere el código de la clase `Notificador` cada vez que se introduce un nuevo medio de notificación. El sistema no permite añadir funcionalidades sin modificar el código base.

### DIP (Dependency Inversion Principle)
Existe una fuerte dependencia entre el código de alto nivel y las clases concretas de bajo nivel (implementaciones de notificación). El sistema no está desacoplado mediante abstracciones, lo que impide que las dependencias sean invertidas hacia interfaces, impidiendo la flexibilidad y la inversión de control.

## B. Explicar por qué el diseño actual es frágil.

El diseño es inherentemente frágil debido al acoplamiento fuerte entre `Notificador` y sus implementaciones concretas. Esto también genera un riesgo de regresión, ya que si se cambia la lógica de un canal (por ejemplo, un cambio en el formato del mensaje de SMS), se pueden generar fallos inesperados en canales que están operando correctamente (como Email), debido a que todos residen en un mismo bloque de código condicional.

## C. Describir los problemas de mantenibilidad del código.

*   **Mantenimiento Centralizado:** La centralización de la lógica en `Notificador` crea un punto único de fallo y de complejidad.
*   **Baja Cohesión:** El código no está agrupado por responsabilidad (como ya se mencionó y se vio en el TP anterior), sino por una estructura condicional, lo que reduce la coherencia.
*   **Complejidad Creciente:** A medida que se añaden más canales, el método `enviar` se convierte en un "monolito" (alto acoplamiento) difícil de leer, depurar y entender.

## D. Explicar cómo impacta esto en el costo del cambio.

El costo del cambio en este sistema es alto y puede crecer de forma exponencial según la cantidad de canales:

*   **Incremento del Esfuerzo y costos exponenciales:** Cada nueva funcionalidad (un nuevo canal de notificación) no solo requiere una nueva implementación, sino la modificación del código central existente, aumentando el riesgo de introducir regresiones, lo que genera un riesgo operacional general.
*   **Aumento del Alcance de Pruebas:** La necesidad de probar la clase completa en lugar de componentes aislados puede aumentar significativamente el esfuerzo de QA y el tiempo de lanzamiento del software.

---
*Este diagnóstico sienta la base para la refactorización necesaria en la Parte B.*