# Nota de diseño (Python idiomático / Protocol): No se requiere importar ni heredar explícitamente de StockObserver.

class AnalyticsObserver:
    """
    Suscriptor concreto de métricas y analítica.
    Satisface estructuralmente el protocolo StockObserver.
    """

    def on_low_stock(self, product_id: str, quantity: int) -> None:
        print(f"Analytics: Evento registrado para {product_id}")
