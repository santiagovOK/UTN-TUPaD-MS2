# Nota de diseño (Python idiomático / Protocol): No se requiere importar ni heredar explícitamente de StockObserver.

class BrokenObserver:
    """
    Suscriptor concreto para prueba de resiliencia ante fallos.
    Lanza intencionalmente un error para comprobar que el bucle
    de notificación del notificador no se detiene.
    """

    def on_low_stock(self, product_id: str, quantity: int) -> None:
        raise RuntimeError("error de red simulado")
