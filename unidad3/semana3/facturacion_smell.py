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