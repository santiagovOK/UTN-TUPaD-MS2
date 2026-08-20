# Metodología de sistemas II - Trabajo Práctico - Unidad 1 (semana3) - Clean Code (Java)

Cree un archivo Markdown para la resolución de cada una de las consignas (principalmente para guiarme yo y poder revisar los cambios trabajo por trabajo en el proyecto.). Pueden verlo aquí: [docs/resolucion_s3.md](docs/resolucion_s3.md)

El informe en PDF solicitado está [aquí](docs/informe.pdf)

Pueden ver el repositorio de la asignatura en https://github.com/santiagovOK/UTN-TUPaD-MS2

---

✨ Estudiante

- Nombre: Varela, Santiago Octavio
- Email institucional: santiago.varela@tupad.utn.edu.ar

---

Tanto la Parte A como la Parte B, además de verla en el código en sí, esta fundamentada en el archivo de resolución citado anteriormente. A continuación se mostrará la resolución de la Parte C y D, que también estará en dicho archivo.

## Parte C - Code Review

A continuación se detalla la revisión técnica del código base original utilizando la checklist obligatoria:

| Pregunta de la Checklist | Evaluación | Justificación |
| :--- | :---: | :--- |
| **¿Los nombres son descriptivos?** | ❌ No | El método se llama `calc` y las variables son letras sueltas (`p`, `o`, `t`, `e`, `r`), sin contexto del dominio médico. |
| **¿Las funciones poseen una única responsabilidad?** | ❌ No | El método asume 4 tareas: suma el precio base, aplica descuentos por profesional, aplica descuentos de obra social y procesa deducciones por turnos. |
| **¿Existe duplicación innecesaria?** | ⚠️ Parcial | Hay estructuras condicionales que podrían simplificarse, aunque el mayor problema es la falta de abstracción. |
| **¿El código es fácilmente extensible?** | ❌ No | Si se desea agregar una nueva regla de facturación (ej: descuento por edad), hay que modificar el código core, rompiendo el principio OCP. |
| **¿Hay manejo correcto de errores?** | ❌ No | Si la lista `estudios` llega como `null`, el bucle `for` lanzará un `NullPointerException`. No se validan los datos. |
| **¿Existe acoplamiento innecesario?** | ❌ Sí | Existe un alto acoplamiento a tipos primitivos (`List<Double>`, `boolean`, `int`) en lugar de depender de objetos del dominio. |
| **¿La cohesión es adecuada?** | ❌ No | La cohesión es baja; el método agrupa lógicas de distintos conceptos (estudios médicos, obras sociales y métricas de turnos). |
| **¿Se respetan principios SOLID?** | ❌ No | Se violan claramente el **Principio de Responsabilidad Única (SRP)** y el **Principio Abierto/Cerrado (OCP)**. |
| **¿El código resulta legible para otro desarrollador?** | ❌ No | Es sumamente críptico. Requiere descifrar qué regla de negocio representa cada *número mágico* (`0.5`, `0.9`, `100`). |

## Parte D - Feedback Profesional

En función del código y sus deficiencias ya descriptas en términos de prácticas clean code, un feedback profesional y técnico podría ser el siguiente:

"Tras la revisión técnica de la clase `Facturacion` y su método `calc`, se identificaron áreas de mejora respecto a la mantenibilidad del código. Actualmente, el método centraliza múltiples responsabilidades (cálculo base y tres reglas de descuentos distintas), lo cual transgrede el Principio de Responsabilidad Única (SRP). Asimismo, la utilización de variables de un solo carácter (`p`, `o`, `t`) omite el contexto del dominio médico, afectando severamente la legibilidad. Se sugiere extraer cada regla de negocio en métodos privados con nomenclatura descriptiva, y consolidar los parámetros de entrada mediante el patrón Parameter Object (por ejemplo, introduciendo una clase `DatosFacturacion`). Estas refactorizaciones favorecerán la extensibilidad del módulo y simplificarán futuras modificaciones."