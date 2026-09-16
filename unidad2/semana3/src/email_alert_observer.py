# Nota de diseño (Python idiomático / Protocol): No se requiere importar ni heredar explícitamente de StockObserver.


class EmailAlertObserver:
    """
    Suscriptor concreto de alertas por email.
    Satisface estructuralmente el protocolo StockObserver.
    """

    def on_low_stock(self, product_id: str, quantity: int) -> None:
        print(f"Alerta Email: Stock bajo para {product_id} ({quantity} unidades)")
