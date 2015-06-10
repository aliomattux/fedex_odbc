from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
from openerp.tools.sql import drop_view_if_exists

class FedExOdbc(osv.osv):
    _name = "fedex.odbc"
    _auto = False

    def init(self, cr):
        drop_view_if_exists(cr, 'fedex_odbc')
        cr.execute("""
                CREATE OR REPLACE VIEW fedex_odbc AS (
                SELECT carrier.fedex_code AS or_sm_id,
                picking.id AS picking_id,
		picking.name AS picking_key,
                picking.id AS or_key,
                address.id AS cu_number,
                picking.name AS or_number,
                CAST('' AS CHAR(128)) AS or_deliver_instruct,
                address.name AS or_ship_name,
                address.street AS or_ship_address1,
                COALESCE(address.phone, CAST('9999999999' AS CHAR(10))) AS or_ship_phone,
                COALESCE(address.phone, CAST('9999999999' AS CHAR(10))) AS customer_phone,
                address.street2 AS or_ship_address2,
                address.city AS or_ship_city,
                country.code AS or_ship_country,
                state.code AS or_ship_state,
                address.zip AS or_ship_postal_code,
                CAST('t' AS BOOLEAN) AS residential,
                COALESCE(address.email, 'noemail@none.com') AS em_address,
                CAST('Y' AS BOOLEAN) AS use_email,
                CAST('email' AS CHAR(15)) AS notification_type,
                CAST('Y' AS BOOLEAN) AS qvn_ship_notification_1,
                CAST ('4' AS CHAR(4)) AS goods_type,
                CAST('Goods' AS CHAR(16)) AS cn22_description
                
                FROM stock_picking picking
                JOIN res_partner address ON (picking.partner_id = address.id)
                LEFT OUTER JOIN res_country_state state ON (address.state_id = state.id)
                LEFT OUTER JOIN res_country country ON (address.country_id = country.id)
                JOIN delivery_carrier carrier ON (picking.carrier_id = carrier.id)
         )""")

    def unlink(self, cr, uid, ids, context=None):
        raise osv.except_osv(_('Error!'), _('You cannot delete any record!'))
