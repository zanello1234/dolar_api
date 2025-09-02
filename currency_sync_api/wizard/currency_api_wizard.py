import requests
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class CurrencyApiWizard(models.TransientModel):
    _name = 'currency.api.wizard'
    _description = 'Listado de monedas disponibles en DolarAPI'

    api_currencies = fields.Text(
        string='Monedas disponibles en DolarAPI', 
        readonly=True,
        help='Lista de tipos de cambio disponibles en la API'
    )

    @api.model
    def get_api_currencies(self):
        """Obtiene el listado de monedas disponibles en DolarAPI"""
        url = 'https://dolarapi.com/v1/dolares'
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            currencies_list = []
            for item in data:
                currencies_list.append(f"• {item['nombre']} - {item.get('casa', 'N/A')}")
            return '\n'.join(currencies_list)
        except Exception as e:
            _logger.error('Error al consultar DolarAPI: %s', str(e))
            return f'Error al consultar la API: {str(e)}'

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if 'api_currencies' in fields:
            res['api_currencies'] = self.get_api_currencies()
        return res
