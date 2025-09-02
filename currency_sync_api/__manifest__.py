{
    'name': 'Currency Sync API',
    'version': '18.0.1.0.0',
    'summary': 'Sincroniza monedas con DolarAPI y actualiza cotizaciones en Odoo',
    'author': 'zanello1234',
    'category': 'Accounting/Accounting',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'views/res_currency_views.xml',
        'views/currency_api_wizard_views.xml',
        'data/currency_sync_cron.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
