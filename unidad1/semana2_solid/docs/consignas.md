# Trabajo Práctico II: SOLID

## Objetivos
* Comprender los principios SOLID.
* Diseñar software flexible y mantenible.
* Reducir acoplamiento y fragilidad.
* Aplicar buenas prácticas de orientación a objetos.
* Mejorar la extensibilidad del sistema.

## Contexto
El Hospital Central continúa evolucionando su sistema de gestión de turnos médicos. Ahora el sistema debe enviar notificaciones a pacientes mediante diferentes canales: email, SMS y WhatsApp.

El diseño actual funciona, pero presenta problemas de escalabilidad y mantenimiento. Cada vez que se agrega un nuevo medio de notificación, el código debe modificarse, aumentando el riesgo de errores y deuda técnica.

El objetivo de este trabajo práctico será rediseñar el sistema aplicando correctamente los principios SOLID.

## Código Base
Se adjunta en un archivo.

## Actividades

### Parte A — Diagnóstico del Diseño
* Indicar qué principios SOLID se están violando.
* Explicar por qué el diseño actual es frágil.
* Describir los problemas de mantenibilidad del código.
* Explicar cómo impacta esto en el costo del cambio.

### Parte B — Refactor Aplicando SOLID
* Rediseñar el sistema aplicando correctamente los principios SOLID.

El nuevo diseño debe incluir:
* Una interfaz Notificacion.
* Implementaciones independientes para cada tipo de notificación.
* Separación clara de responsabilidades.
* Desacoplamiento entre clases.

#### Ejemplo esperado
```java
public interface Notificacion {

    void enviar(String mensaje);
}
```

#### Implementaciones mínimas requeridas
* EmailNotificacion
* SmsNotificacion
* WhatsappNotificacion

### Parte C — Extensibilidad
El hospital desea agregar nuevos medios de comunicación.

Incorporar:
* TelegramNotificacion
* PushNotificacion

Condición obligatoria: Las nuevas funcionalidades deben agregarse sin modificar las clases existentes.

### Parte D — Dependency Inversion Principle (DIP)
Crear una clase llamada GestorTurnos. (`public class GestorTurnos`)
Esta clase deberá depender de abstracciones y no de implementaciones concretas.

El sistema debe permitir cambiar fácilmente el mecanismo de notificación.

## Requisitos Técnicos
* Utilizar Java orientado a objetos.
* Aplicar encapsulamiento correctamente.
* Evitar condicionales innecesarios.
* Utilizar polimorfismo.
* El diseño debe ser extensible y mantenible.
* Sugerencia: Se recomienda utilizar composición e interfaces para reducir acoplamiento.

## Entregables
* Documento PDF explicando los principios SOLID aplicados.
* Diagrama UML simple del diseño propuesto.
* Código fuente completo en Java.
* Ejemplos de ejecución del sistema.

## Criterios de Evaluación
| Criterio | Puntaje |
| :--- | :--- |
| Aplicación correcta de SOLID | 50% |
| Diseño desacoplado y mantenible | 25% |
| Extensibilidad del sistema | 15% |
| Explicación técnica y UML | 10% |