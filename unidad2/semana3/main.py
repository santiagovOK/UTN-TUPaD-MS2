"""
Punto de entrada principal del sistema y código de prueba.

Ensambla los componentes desacoplados del patrón Observer y ejecuta
la simulación integral para demostrar:
  1. Registro y suscripción de observadores.
  2. Resiliencia ante fallos con manejo de errores dentro del bucle (BrokenObserver).
  3. Gestión dinámica del ciclo de vida con unsubscribe.
"""

import logging
from src.inventory_manager import InventoryManager
from src.email_alert_observer import EmailAlertObserver
from src.analytics_observer import AnalyticsObserver
from src.broken_observer import BrokenObserver
from src.replenish_observer import ReplenishObserver
from src.push_notification_observer import PushNotificationObserver


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    print("=== Código de prueba: suscripción de observadores ===")
    manager = InventoryManager()

    # Instanciación independiente de observadores concretos
    email_obs = EmailAlertObserver()
    analytics_obs = AnalyticsObserver()
    broken_obs = BrokenObserver()
    replenish_obs = ReplenishObserver()
    push_obs = PushNotificationObserver()

    # Suscripción de observadores al gestor de inventario
    manager.subscribe(email_obs)
    manager.subscribe(analytics_obs)
    manager.subscribe(broken_obs)
    manager.subscribe(replenish_obs)
    manager.subscribe(push_obs)
    print("Observadores registrados exitosamente en InventoryManager.\n")

    # Demostración de resiliencia: BrokenObserver lanza excepción sin frenar la cadena
    print("=== Ejecución de prueba de resiliencia (BrokenObserver) ===")
    print("Actualizando stock de PROD-001 a 5 unidades (umbral < 10):")
    manager.update_stock("PROD-001", 5)

    # Demostración de ciclo de vida: desuscripción dinámica de un observador
    print("\n=== Demostración de desuscripción dinámica (unsubscribe) ===")
    print("Desuscribiendo PushNotificationObserver.")
    manager.unsubscribe(push_obs)

    print("Actualizando stock de PROD-002 a 3 unidades (umbral < 10):")
    manager.update_stock("PROD-002", 3)
    print("\nSimulación finalizada con éxito.")


if __name__ == "__main__":
    main()
