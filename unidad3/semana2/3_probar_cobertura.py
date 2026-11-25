def autorizar_reintegro(
    antiguedad_meses: int, monto: float, tiene_sanciones: bool
) -> bool:
    """Evalúa la aprobación automática de un reintegro médico."""
    autorizado = False

    if antiguedad_meses > 6 and monto <= 50000.0:
        if not tiene_sanciones:
            autorizado = True

    return autorizado


def ejecutar_suite_cobertura():
    # TC-01: True, True -> True (Ramas 1 y 3)
    assert autorizar_reintegro(12, 30000.0, False) is True, "Fallo en TC-01"

    # TC-02: True, False -> False (Ramas 1 y 4)
    assert autorizar_reintegro(12, 30000.0, True) is False, "Fallo en TC-02"

    # TC-03: False (antigüedad <= 6) -> False (Rama 2)
    assert autorizar_reintegro(3, 30000.0, False) is False, "Fallo en TC-03"

    # TC-04: False (monto > 50000) -> False (Rama 2)
    assert autorizar_reintegro(12, 75000.0, False) is False, "Fallo en TC-04"

    print(
        "Todos los casos del Punto 3 pasaron exitosamente (100% de ramas cubiertas)."
    )


if __name__ == "__main__":
    ejecutar_suite_cobertura()