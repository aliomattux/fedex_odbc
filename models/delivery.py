from openerp.osv import osv, fields


class DeliveryCarrier(osv.osv):
    _inherit = 'delivery.carrier'
    _columns = {
	'fedex_code': fields.char('FedEx Shipment Code'),
    }
