# Nota de diseño (Python idiomático / Protocol): No se requiere importar ni heredar explícitamente de StockObserver.

class ReplenishObserver:
    """
    Suscriptor concreto de reposición automática.
    Satisface estructuralmente el protocolo StockObserver.
    """

    def on_low_stock(self, product_id: str, quantity: int) -> None:
        print(f"Reposición: Orden emitida por 100 unidades para {product_id}")
