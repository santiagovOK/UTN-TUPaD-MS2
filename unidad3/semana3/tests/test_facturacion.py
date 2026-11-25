import pytest
from src.facturacion import liquidar_consulta


def test_liquidar_consulta_osde_sin_urgencia():
    arancel = 10000.0
    obra_social = "OSDE"
    es_urgencia = False

    total = liquidar_consulta(arancel, obra_social, es_urgencia)

    assert total == pytest.approx(6000.0)


def test_liquidar_consulta_particular_con_urgencia():
    arancel = 12000.0
    obra_social = "particular"
    es_urgencia = True

    total = liquidar_consulta(arancel, obra_social, es_urgencia)

    assert total == pytest.approx(14500.0)


def test_liquidar_consulta_arancel_no_positivo():
    with pytest.raises(ValueError, match="El arancel base debe ser positivo"):
        liquidar_consulta(0.0, "OSDE")


def test_liquidar_consulta_obra_social_no_conveniada():
    with pytest.raises(ValueError, match="Obra social no conveniada"):
        liquidar_consulta(10000.0, "MEDICUS")
