# Sujeto / Notificador
#
# Gestión dinámica de observadores desacoplado de clases concretas:
#   - #_observers: list[StockObserver]
#   - subscribe(observer) / unsubscribe(observer)
#   - _notify(product_id, quantity) con manejo de excepciones por observador
#     (captura de errores DENTRO del loop).
#

