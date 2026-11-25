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