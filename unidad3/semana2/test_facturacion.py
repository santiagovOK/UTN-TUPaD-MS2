"""Pruebas unitarias para calcular_arancel_consulta siguiendo el patrón AAA."""

import pytest
from facturacion import calcular_arancel_consulta


def test_calcular_arancel_aplica_cobertura_osde_sin_urgencia():
    # Arrange (Configuración de precondiciones y datos teóricos)
    arancel_base = 10000.0
    obra_social = "OSDE"
    es_urgencia = False
    valor_esperado = 6000.0

    # Act (Ejecución de la función bajo examen)
    valor_obtenido = calcular_arancel_consulta(
        arancel_base, obra_social, es_urgencia
    )

    # Assert (Aseveración del resultado)
    assert valor_obtenido == pytest.approx(valor_esperado, rel=1e-3)


def test_calcular_arancel_paciente_particular_con_recargo_de_urgencia():
    # Arrange
    arancel_base = 12000.0
    obra_social = "particular"
    es_urgencia = True
    valor_esperado = 14500.0

    # Act
    valor_obtenido = calcular_arancel_consulta(
        arancel_base, obra_social, es_urgencia
    )

    # Assert
    assert valor_obtenido == pytest.approx(valor_esperado, rel=1e-3)


def test_calcular_arancel_con_arancel_negativo_lanza_excepcion():
    # Arrange
    arancel_invalido = -500.0
    obra_social = "SWISS"

    # Act & Assert (Evaluación del desvío de borde)
    with pytest.raises(ValueError) as context:
        calcular_arancel_consulta(arancel_invalido, obra_social)

    assert "arancel base debe ser estrictamente positivo" in str(context.value)


def test_calcular_arancel_con_obra_social_desconocida_lanza_excepcion():
    # Arrange
    arancel_base = 8000.0
    obra_social_invalida = "MEDICUS"

    # Act & Assert
    with pytest.raises(ValueError) as context:
        calcular_arancel_consulta(arancel_base, obra_social_invalida)

    assert "Obra social no conveniada" in str(context.value)