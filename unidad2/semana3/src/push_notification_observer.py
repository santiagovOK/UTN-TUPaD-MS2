# Nota de diseño (Python idiomático / Protocol): No se requiere importar ni heredar explícitamente de StockObserver.

class PushNotificationObserver:
    """
    Suscriptor concreto de notificaciones push.
    Demuestra que el sistema es extensible sin tocar el InventoryManager
    ni requerir herencia nominal.
    """

    def on_low_stock(self, product_id: str, quantity: int) -> None:
        print(f"Push: Notificación enviada al móvil para {product_id}")
