# UML — Situación inicial: `InventoryManager` acoplado

El gestor de inventario construye y conoce directamente los tres servicios de notificación. Como sus ciclos de vida nacen dentro del gestor, las relaciones son composiciones; añadir o cambiar un canal obliga a modificar `InventoryManager`.

```mermaid
classDiagram
    direction LR

    class InventoryManager {
        #_stock dict~str, int~
        #_email_service EmailAlertService
        #_analytics AnalyticsDashboard
        #_replenishment AutoReplenishment
        +update_stock(product_id: str, quantity: int) None
        +sell_product(product_id: str, sold: int) None
    }

    class EmailAlertService {
        +send_low_stock_alert(product_id: str, quantity: int) None
    }

    class AnalyticsDashboard {
        +record_low_stock_event(product_id: str) None
    }

    class AutoReplenishment {
        +trigger_order(product_id: str, quantity: int) None
    }

    InventoryManager *-- EmailAlertService : crea y usa
    InventoryManager *-- AnalyticsDashboard : crea y usa
    InventoryManager *-- AutoReplenishment : crea y usa
```
