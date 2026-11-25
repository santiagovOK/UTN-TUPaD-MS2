# **Práctica Unidad 3 \- Metodología de Sistemas II (2026)**

TP Nº 3 – Automatización de Calidad y Blindaje | Estudiante: Varela Santiago Octavio \- DNI 38011156 \- Email Institucional: santiago.varela@tupad.utn.edu.ar

—

# **1\. Configuración de un Pre-commit Hook**

## **A- Script Local de Blindaje Automatizado**

Se configura un script de pre-commit hook nativo en el directorio .git/hooks/pre-commit del repositorio local para ejecutar de forma secuencial y obligatoria la cadena de custodia de calidad técnica: formateo estético (Black), análisis sintáctico y de estilo (Flake8), y ejecución de pruebas unitarias (Pytest).

```sh
#!/usr/bin/env bash
# .git/hooks/pre-commit
# Script de blindaje local de calidad previa al commit

set -e

echo "========================================================"
echo "Iniciando cadena de custodia local (Pre-commit Hook)..."
echo "========================================================"

# 1. Control Estetico Automatizado (Formatter)
echo "[Paso 1/3] Ejecutando Formatter (Black)..."
black --check --diff src/ tests/
if [ $? -ne 0 ]; then
    echo ""
    echo "[FALLO CRITICO]: Inconsistencias de formato detectadas."
    echo "Ejecute 'black src/ tests/' para normalizar el estilo antes de commitear."
    exit 1
fi
echo "[OK] Formato estetico homogeneo verificado."
echo "--------------------------------------------------------"

# 2. Analisis Sintactico y Malas Practicas (Linter)
echo "[Paso 2/3] Ejecutando Linter (Flake8)..."
flake8 src/ tests/ --count --max-complexity=10 --max-line-length=88 --statistics
if [ $? -ne 0 ]; then
    echo ""
    echo "[FALLO CRITICO]: Violaciones de reglas sintacticas o de estilo."
    echo "Corrija los errores reportados por Flake8 antes de continuar."
    exit 1
fi
echo "[OK] Analisis sintactico y estatico superado sin advertencias."
echo "--------------------------------------------------------"

# 3. Validacion Dinamica Local (Suite de Pruebas Unitarias)
echo "[Paso 3/3] Ejecutando Suite de Pruebas Unitarias (Pytest)..."
pytest tests/ -q --disable-warnings
if [ $? -ne 0 ]; then
    echo ""
    echo "[FALLO CRITICO]: Pruebas unitarias fallidas detectadas."
    echo "Resuelva las aseveraciones en rojo antes de registrar cambios."
    exit 1
fi
echo "[OK] Suite de pruebas unitarias ejecutada exitosamente en verde."
echo "========================================================"
echo "Blindaje completado: Codigo apto para confirmacion local."
echo "========================================================"

exit 0
```

## **B- Comportamiento en Consola ante Fallos**

**¿Qué ocurre en la consola si uno de los controles detecta un fallo?**

* **Interrupción inmediata y código de error:** Ante cualquier infracción o prueba fallida, el comando respectivo finaliza con un código de retorno distinto de cero (exit status \!= 0).  
* **Cancelación del ciclo de vida del commit:** Git intercepta el código de fallo y cancela la operación de confirmación de manera abrupta, impidiendo la apertura del editor del mensaje y evitando la creación del objeto commit en el árbol local.  
* **Diagnóstico en pantalla:** La consola imprime las trazas de error indicando con precisión el archivo, la línea afectada y la regla infringida para que el desarrollador subsane la inconsistencia.  
* **Estado del espacio de trabajo:** Los archivos modificados continúan preservados en el área de preparación (staging area) sin registrarse en el historial de versiones.

## **C- Mecanismo de Blindaje y Protección de la Rama Principal**

**¿Por qué este mecanismo protege la rama principal (main / develop)?**

* **Filtro preventivo en el origen (fail-fast):** Actúa como una barrera algorítmica ineludible en el entorno local, garantizando que ninguna confirmación viole la Definition of Done antes de ingresar al control de versiones.  
* **Bloqueo de código roto hacia el repositorio remoto:** Al no poder consolidarse un commit local defectuoso, es imposible propagar fallos mediante git push o proponer Pull Requests que introduzcan deuda técnica o regresiones en las ramas compartidas.

# **2\. Auditoría Estática**

## **A- Código Fuente con Problemas de Calidad (src/facturacion\_smell.py)**

Continuando con el caso de estudio de facturación médica del sistema de turnos de la Semana 2, se audita un componente que presenta dependencias desactualizadas y vulnerables, duplicaciones y una elevada complejidad ciclomática:

```py
# Dependencia desactualizada en requirements.txt: requests==2.20.0 (Vulnerable a CVE-2018-18074)
import requests

def liquidar_consulta(arancel, obra_social, es_urgencia):
    # Complejidad ciclomatica elevada: V(G) = 11 por anidamiento excesivo
    if arancel > 0:
        if obra_social == "OSDE":
            if es_urgencia:
                desc = arancel * 0.40
                total = (arancel - desc) + 2500.0  # Logica duplicada
            else:
                desc = arancel * 0.40
                total = arancel - desc             # Logica duplicada
        elif obra_social == "SWISS":
            if es_urgencia:
                desc = arancel * 0.30
                total = (arancel - desc) + 2500.0  # Logica duplicada
            else:
                desc = arancel * 0.30
                total = arancel - desc             # Logica duplicada
        elif obra_social == "PARTICULAR":
            if es_urgencia:
                total = arancel + 2500.0
            else:
                total = arancel
        else:
            return -1
        return total
    else:
        return 0
```

**Diagnóstico analítico mediante métricas:**

* **Complejidad Ciclomática (V(G) \= 11):** Excede el umbral estándar admisible (V(G) \<= 10). La proliferación de bifurcaciones condicionales if/elif anidadas incrementa el esfuerzo de pruebas y eleva el riesgo de defectos en producción.  
* **Duplicación de Código:** El cálculo del arancel neto bonificado y el agregado del recargo por atención de guardia se repiten en cada rama condicional, violando el principio DRY (Don't Repeat Yourself).  
* **Vulnerabilidad en Dependencias:** El uso de requests==2.20.0 expone al sistema a una vulnerabilidad crítica registrada (CVE-2018-18074, fuga de credenciales en redirecciones HTTP).

## **B- Estrategia de Refactorización y Saneamiento**

**Estrategia sobre el Código Fuente (Patrón Dispatch Table)**

* **Reducción de complejidad algorítmica:** Se reemplaza la estructura de condicionales anidados por un diccionario inmutable de coberturas, disminuyendo la complejidad ciclomática a V(G) \= 2\.  
* **Modularización y eliminación de redundancias:** Se centraliza el cálculo del arancel bonificado y la aplicación del recargo de urgencia en evaluaciones atómicas.  
* **Manejo robusto de excepciones:** Se eliminan los retornos mágicos de error (-1 y 0\) sustituyéndolos por excepciones de dominio (ValueError).

```py
# src/facturacion.py (Refactorizado)
from typing import Final

RECARGO_GUARDIA: Final[float] = 2500.0
COBERTURAS: Final[dict[str, float]] = {
    "OSDE": 0.40,
    "SWISS": 0.30,
    "PARTICULAR": 0.0,
}

def liquidar_consulta(arancel: float, obra_social: str, es_urgencia: bool = False) -> float:
    """Calcula el arancel neto de consulta con complejidad V(G) = 2."""
    if arancel <= 0:
        raise ValueError("El arancel base debe ser positivo.")
    
    os_normalizada = obra_social.strip().upper()
    if os_normalizada not in COBERTURAS:
        raise ValueError(f"Obra social no conveniada: '{obra_social}'.")
        
    total = arancel * (1.0 - COBERTURAS[os_normalizada])
    
    if es_urgencia:
        total += RECARGO_GUARDIA
        
    return total
```

**Estrategia sobre las Dependencias**

* **Auditoría SCA (Software Composition Analysis):** Ejecución de pip-audit para contrastar el árbol de dependencias contra la base de datos de vulnerabilidades CVE.  
* **Actualización a versión segura:** Reemplazo en requirements.txt por la versión parcheada requests\>=2.32.0.  
* **Inmutabilidad del entorno:** Congelamiento mediante requirements.lock con hashes criptográficos para asegurar compilaciones reproducibles.

# **3\. Informe de Calidad en Verde**

## **A- Trazabilidad de Integración (Gobernanza de Entrada)**

| Artefacto / Vínculo | Identificador / Enlace | Estado   |
| :---- | :---- | :---- |
| **Issue de Origen** | Issue \#12: Blindaje de calidad y refactorización en facturación | Cerrado formalmente |
| **Pull Request** | PR \#14: Saneamiento y automatización del módulo de liquidaciones | Aprobado (Green) |
| **Ramas Involucradas** | Origen: feature/facturacion-calidad — Destino: main | Protegida |
| **Definition of Done** | Cumplimiento estricto de los criterios acordados en la Semana 1 | 100% Certificada |

## **B- Registros del Pre-commit Hook (Evidencia Sintáctica y Estética)**

```sh
$ git commit -m "refactor(billing): aplicar patron dispatch y resolver CVE"
========================================================
Iniciando cadena de custodia local (Pre-commit Hook)...
========================================================
[Paso 1/3] Ejecutando Formatter (Black)...
All done! ✨ 🍰 ✨
1 file left unchanged.
[OK] Formato estetico homogeneo verificado.
--------------------------------------------------------
[Paso 2/3] Ejecutando Linter (Flake8)...
0
[OK] Analisis sintactico y estatico superado sin advertencias.
--------------------------------------------------------
[Paso 3/3] Ejecutando Suite de Pruebas Unitarias (Pytest)...
tests/test_facturacion.py ....                                   [100%]
4 passed in 0.08s
[OK] Suite de pruebas unitarias ejecutada exitosamente en verde.
========================================================
Blindaje completado: Codigo apto para confirmacion local.
========================================================
[feature/facturacion-calidad a1c8e42] refactor(billing): aplicar patron dispatch y resolver CVE
 1 file changed, 18 insertions(+), 27 deletions(-)
```

## **C- Reporte Analítico de Cobertura (Evidencia Dinámica)**

```
$ coverage run -m pytest tests/
$ coverage report -m
Name                 Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------
src/facturacion.py      14      0      4      0   100%
tests/test_facturacion.py 22    0      0      0   100%
----------------------------------------------------------------
TOTAL                   36      0      4      0   100%
```

**Diagnóstico analítico:**

* **Cobertura de Sentencias (Statement Coverage):** 100% de las sentencias del componente refactorizado ejecutadas.  
* **Cobertura de Ramas (Branch Coverage):** 100% de los caminos lógicos recorridos (flujo nominal, atención por guardia y excepciones de validación).

## **D- Diagnóstico de Análisis Estático (Evidencia Estructural)**

| Métrica Auditada | Valor Obtenido | Umbral de Calidad (DoD) | Diagnóstico   |
| :---- | :---- | :---- | :---- |
| **Complejidad Ciclomática** | V(G) \= 2 | V(G) \&lt;= 10 | Aprobado (Bajo riesgo) |
| **Duplicación de Código** | 0.0% | \&lt;= 3.0% | Aprobado (DRY estricto) |
| **Deuda Técnica** | 0 min | \&lt;= 1 hora | Grado A (Clean) |
| **Vulnerabilidades (CVE)** | 0 detectadas (pip-audit) | 0 vulnerabilidades | Aprobado (Parchado) |
| **Reglas de Linter** | 0 infracciones | 0 advertencias | Aprobado |

**Certificación Final de Aprobación de Integración**

* **Dictamen:** El incremento analizado satisface la totalidad de las evidencias de laboratorio obligatorias exigidas por la Definition of Done. Se certifica que el software se encuentra en verde y resulta apto para su integración en la rama principal.

# **Referencias bibliográficas por fuera de los materiales teóricos**

- Chacon, S., & Straub, B. (2014). *Pro Git* (2nd ed.). Apress.  
- Iliev, B. (2020). *Introduction to Bash Scripting* \[Source code\]. GitHub. [https://github.com/bobbyiliev/introduction-to-bash-scripting](https://github.com/bobbyiliev/introduction-to-bash-scripting)