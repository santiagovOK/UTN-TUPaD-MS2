"""Módulo de servicios de facturación para el sistema de turnos."""

from typing import Final

RECARGO_URGENCIA_GUARDIA: Final[float] = 2500.0
COBERTURAS_OBRAS_SOCIALES: Final[dict[str, float]] = {
    "OSDE": 0.40,
    "SWISS": 0.30,
    "PARTICULAR": 0.0,
}


def calcular_arancel_consulta(
    arancel_base: float, obra_social: str, es_urgencia: bool = False
) -> float:
    """Calcula el arancel neto de una consulta médica."""
    if arancel_base <= 0:
        raise ValueError("El arancel base debe ser estrictamente positivo.")

    if not obra_social or not obra_social.strip():
        raise ValueError("La obra social especificada no puede estar vacía.")

    nombre_normalizado = obra_social.strip().upper()
    if nombre_normalizado not in COBERTURAS_OBRAS_SOCIALES:
        raise ValueError(
            f"Obra social no conveniada en el padrón activo: '{obra_social}'."
        )

    porcentaje_cobertura = COBERTURAS_OBRAS_SOCIALES[nombre_normalizado]
    monto_bonificado = arancel_base * (1.0 - porcentaje_cobertura)

    if es_urgencia:
        return monto_bonificado + RECARGO_URGENCIA_GUARDIA

    return monto_bonificado