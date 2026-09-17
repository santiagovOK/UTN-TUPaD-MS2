import logging
from src.stock_observer import StockObserver


class InventoryManager:
    """
    Sujeto / Notificador del inventario.

    Diseño desacoplado (GoF - Observer):
    No utiliza referencia nominal, importación o instanciación directa
    de servicios concretos (EmailAlertService, AnalyticsDashboard, AutoReplenishment, etc.).
    Solo se comunica y tipa a través del protocolo genérico StockObserver.
    """

    def __init__(self) -> None:
        self._observers: list[StockObserver] = []
        self._stock: dict[str, int] = {}

    def subscribe(self, observer: StockObserver) -> None:
        """
        Registra un nuevo observador en la lista si no está previamente agregado.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: StockObserver) -> None:
        """
        Remueve un observador de la lista si se encuentra presente.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify(self, product_id: str, quantity: int) -> None:
        """
        Notifica síncronamente a todos los observadores registrados.
        Aislamiento de fallos (Fail-Safe Loop):
        El bloque try/except envuelve cada llamada individual dentro del bucle
        para que un observador defectuoso no detenga la notificación del resto.
        """
        for observer in self._observers:
            try:
                observer.on_low_stock(product_id, quantity)
            except Exception as e:
                logging.error(f"Error notificando al observador {type(observer).__name__}: {e}")

    def update_stock(self, product_id: str, quantity: int) -> None:
        """
        Actualiza el nivel de stock de un producto.
        Si la cantidad cae por debajo del umbral crítico (< 10), dispara la notificación.
        """
        self._stock[product_id] = quantity
        if quantity < 10:
            self._notify(product_id, quantity)

    def sell_product(self, product_id: str, sold: int) -> None:
        """
        Registra la venta de unidades de un producto reduciendo su stock disponible.

        Nota de diseño y no regresión:
        Si bien este método no se reitera en el "Pseudocódigo de la solución" de las consignas, se preserva
        por tratarse de una funcionalidad de negocio preexistente del código original problemático.
        Se refactoriza para reutilizar el método centralizado _notify(), evitando duplicación
        de lógica y eliminando las dependencias rígidas anteriores.

        Evita valores negativos de stock.
        Si el stock resultante es menor a 10 unidades, notifica a los observadores.
        """
        new_quantity = max(0, current_stock - sold)
        self._stock[product_id] = new_quantity
        if new_quantity < 10:
            self._notify(product_id, new_quantity)
