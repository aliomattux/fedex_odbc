from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
from openerp.tools.sql import drop_view_if_exists

class FedExCustomsOdbc(osv.osv):
    _name = "wfedex.customs.odbc"
    _auto = False
    _columns = {
	'package_id': fields.char('Package'),
	'goods_type': fields.char('Goods Type', size=4),
	'cn22_description': fields.char('CN22 Description', size=128),
	'description_of_good': fields.char('Description of Good'),
	'unit_price': fields.float('Unit Price'),
    }

    def init(self, cr):
        drop_view_if_exists(cr, 'fedex_customs_odbc')
        cr.execute("""
                CREATE OR REPLACE VIEW fedex_customs_odbc AS (
                SELECT picking.id, CAST('Goods' AS CHAR(16)) AS description_of_good,
                CAST('9.99' AS FLOAT) AS unit_price, CAST (1 AS INT) AS units, CAST('EA' AS CHAR(5)) AS unit_of_measure,
		CAST('US' AS CHAR(5)) AS country_of_origin
                FROM stock_picking picking
         )""")

    def unlink(self, cr, uid, ids, context=None):
        raise osv.except_osv(_('Error!'), _('You cannot delete any record!'))

