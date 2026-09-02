# Resolución Unidad 2 - Semana 1: Estructura en Python

## 1. Diagrama UML Inicial

Diagrama UML de clases correspondiente a la situación problemática inicial (antes del refactoring). Este diagrama muestra el acoplamiento directo entre `ReportService` y los distintos reportes concretos (`PDFReport`, `ExcelReport`, `CSVReport`).

👉 **Ver diagrama:** [uml/diagrama_inicial.md](../uml/diagrama_inicial.md)

---

A continuación se presenta la estructura de archivos tentativa para la implementación en Python del patrón Factory Method (variante Static / Simple Factory), basada en el pseudocódigo propuesto. En esta etapa solo se definen los esqueletos de las clases y métodos (sin la lógica interna).

## Estructura de Directorios

```text
src/
├── reports/
│   ├── __init__.py
│   ├── report.py           # Interfaz / Clase base
│   ├── pdf_report.py       # Producto concreto
│   ├── excel_report.py     # Producto concreto
│   ├── csv_report.py       # Producto concreto
│   └── html_report.py      # Producto concreto (nuevo)
├── factories/
│   ├── __init__.py
│   └── report_factory.py   # Creador (Fábrica estática)
├── services/
│   ├── __init__.py
│   └── report_service.py   # Servicio agnóstico al formato
└── main.py                 # Punto de entrada / Cliente
```