# Nota de diseño (Python idiomático / Protocol): No se requiere importar ni heredar explícitamente de StockObserver.

class PushNotificationObserver:
    """
    Suscriptor concreto de notificaciones push.
    Demuestra la extensibilidad del sistema (Open/Closed Principle)
    sin requerir modificaciones en InventoryManager ni herencia nominal.
    """

    def on_low_stock(self, product_id: str, quantity: int) -> None:
        print(f"Push: Notificación enviada al móvil para {product_id}")
