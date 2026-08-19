# 🚀 Trabajo Práctico III: "Clean Code / Code Review"

## Objetivos

- Aplicar principios de Clean Code.
- Mejorar legibilidad y mantenibilidad.
- Aplicar técnicas de refactoring seguro.
- Comprender cohesión y acoplamiento.
- Realizar revisiones profesionales de código.
- Desarrollar criterios técnicos de calidad.

## Contexto

El Hospital Central incorporó recientemente un módulo de facturación médica desarrollado por distintos programadores a lo largo del tiempo.

Aunque el sistema funciona correctamente, el código presenta problemas de legibilidad, baja cohesión y alto acoplamiento, dificultando el mantenimiento y la evolución futura del software.

El objetivo de este trabajo práctico será mejorar la calidad del código, aplicar técnicas de refactoring seguro y realizar un proceso formal de code review.

## Código Base

Se adjunta en un archivo.

## Actividades

### Parte A — Clean Code

Refactorizar el código aplicando principios de Clean Code.

Mejorar al menos:

- Nombres de clases, métodos y variables.
- Legibilidad general.
- Separación de responsabilidades.
- Cohesión interna.
- Reducción de acoplamiento.
- Manejo de errores.

**Importante:** El comportamiento funcional del sistema no debe modificarse.

### Parte B — Refactoring Seguro

Aplicar técnicas de refactoring seguro sobre el código original.

Implementar obligatoriamente:

- Extract Method
- Introduce Parameter Object
- Move Method

Explicar brevemente:

- Qué problema resolvía cada técnica.
- Qué mejora aporta al diseño.

### Parte C — Code Review

Realizar una revisión técnica del código utilizando una checklist profesional.

**Checklist mínima obligatoria:**

- ¿Los nombres son descriptivos?
- ¿Las funciones poseen una única responsabilidad?
- ¿Existe duplicación innecesaria?
- ¿El código es fácilmente extensible?
- ¿Hay manejo correcto de errores?
- ¿Existe acoplamiento innecesario?
- ¿La cohesión es adecuada?
- ¿Se respetan principios SOLID?
- ¿El código resulta legible para otro desarrollador?

### Parte D — Feedback Profesional

Simular un proceso real de revisión entre desarrolladores.

Elaborar feedback técnico profesional sobre el código revisado.

> **Ejemplo de feedback esperado:**
> La función presenta múltiples responsabilidades, lo que dificulta su mantenibilidad. Se recomienda separar el cálculo de descuentos y promociones en métodos independientes para mejorar cohesión y facilitar futuras extensiones.

**Importante:** El feedback debe ser técnico, objetivo y profesional. No deben utilizarse comentarios despectivos o personales.

## Requisitos Técnicos

- Utilizar Java orientado a objetos.
- Aplicar buenas prácticas de Clean Code.
- Mantener compatibilidad funcional.
- Organizar correctamente clases y métodos.
- Entregar código legible y correctamente indentado.

## Entregables

- Código fuente refactorizado.
- Documento PDF explicando las mejoras realizadas.
- Checklist de code review completa.
- Feedback profesional del code review.

## Criterios de Evaluación

| Criterio | Puntaje |
|----------|---------|
| Aplicación de Clean Code | 30% |
| Refactoring correcto y seguro | 30% |
| Calidad del code review | 25% |
| Feedback técnico profesional | 15% |
