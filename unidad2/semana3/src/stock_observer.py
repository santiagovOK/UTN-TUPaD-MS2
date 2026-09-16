from typing import Protocol


class StockObserver(Protocol):
    """
    Protocolo estructural que define la interfaz suscriptora común (GoF).
    Cualquier observador debe implementar este método para recibir notificaciones
    de eventos de stock bajo.
    """

    def on_low_stock(self, product_id: str, quantity: int) -> None:
        """
        Método de notificación invocado cuando el stock de un producto cae por debajo del umbral.

        :param product_id: Identificador del producto.
        :param quantity: Cantidad actual de stock restante.
        """
        ...
