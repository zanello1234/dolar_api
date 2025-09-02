# Currency Sync API

Sincroniza automáticamente las cotizaciones de monedas en Odoo 18 usando la API de https://dolarapi.com.

## Características
- Permite conectar cualquier moneda de Odoo con los tipos de cambio de DolarAPI (oficial, blue, mayorista, etc.)
- El usuario puede crear nuevas monedas (ejemplo: Dólar Blue) y vincularlas con el campo `Código DolarAPI`.
- Actualización automática diaria a las 22:00 mediante tarea programada (cron).
- Actualiza el campo de cotización (`rate`) en el modelo `res.currency`.

## Instalación
1. Copia la carpeta `currency_sync_api` en tu carpeta de addons de Odoo.
2. Instala el módulo desde el menú de aplicaciones de Odoo.

## Configuración
1. Ve a **Configuración > Monedas**.
2. Edita o crea una moneda y completa el campo `Código DolarAPI` con el nombre exacto de la moneda en la API (ejemplo: `oficial`, `blue`, `mayorista`).
3. Guarda los cambios.

## Funcionamiento
- Todos los días a las 22:00 el sistema consulta la API y actualiza las cotizaciones de las monedas conectadas.
- Puedes ejecutar la sincronización manualmente llamando al método `sync_dolarapi_currencies` desde el modelo `res.currency`.

## Ejemplo de uso
- Para conectar el Dólar Blue, crea una moneda en Odoo y pon `blue` en el campo `Código DolarAPI`.

## Requisitos
- Odoo 18
- Acceso a internet para consultar la API
- El módulo utiliza la librería `requests` (asegúrate de que esté instalada en el entorno de Odoo)

## Autor
zanello1234
