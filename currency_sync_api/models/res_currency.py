import requests
import logging
from odoo import models, fields, api
from datetime import datetime

_logger = logging.getLogger(__name__)

class ResCurrency(models.Model):
    _inherit = 'res.currency'

    dolarapi_code = fields.Selection(
        string='Código DolarAPI',
        selection='_get_dolarapi_codes',
        help='Selecciona el tipo de cambio de DolarAPI para esta moneda.'
    )

    @api.model
    def _get_dolarapi_codes(self):
        """Obtiene la lista de monedas disponibles en DolarAPI"""
        url = 'https://dolarapi.com/v1/dolares'
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return [(item['nombre'], item['nombre'].title()) for item in data]
        except Exception as e:
            _logger.warning('Error al consultar DolarAPI: %s', str(e))
            return [('oficial', 'Oficial'), ('blue', 'Blue')]

    @api.model
    def sync_dolarapi_currencies(self):
        """Sincroniza las cotizaciones de monedas desde DolarAPI"""
        url = 'https://dolarapi.com/v1/dolares'
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Actualizar cotizaciones para monedas configuradas
            currencies = self.search([('dolarapi_code', '!=', False)])
            today = fields.Date.today()
            
            for currency in currencies:
                api_item = next((item for item in data if item['nombre'] == currency.dolarapi_code), None)
                if api_item and api_item.get('venta'):
                    try:
                        rate_value = float(api_item['venta'])
                        if rate_value > 0:
                            # Buscar si ya existe una cotización para hoy
                            existing_rate = self.env['res.currency.rate'].search([
                                ('currency_id', '=', currency.id),
                                ('name', '=', today)
                            ], limit=1)
                            
                            # En Odoo, rate es 1/valor_real para monedas extranjeras
                            inverse_rate = 1.0 / rate_value
                            
                            if existing_rate:
                                # Actualizar cotización existente
                                existing_rate.write({'rate': inverse_rate})
                                _logger.info('Actualizada cotización existente %s: %s (rate: %s)', 
                                           currency.name, rate_value, inverse_rate)
                            else:
                                # Crear nueva cotización
                                self.env['res.currency.rate'].create({
                                    'currency_id': currency.id,
                                    'name': today,
                                    'rate': inverse_rate,
                                    'company_id': self.env.company.id,
                                })
                                _logger.info('Creada nueva cotización %s: %s (rate: %s)', 
                                           currency.name, rate_value, inverse_rate)
                                
                    except (ValueError, TypeError) as e:
                        _logger.warning('Error al procesar cotización para %s: %s', currency.name, str(e))
                        
        except Exception as e:
            _logger.error('Error al sincronizar monedas desde DolarAPI: %s', str(e))
