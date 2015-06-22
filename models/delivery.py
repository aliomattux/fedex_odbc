from openerp.osv import osv, fields


class DeliveryCarrier(osv.osv):
    _inherit = 'delivery.carrier'
    _columns = {
	'fedex_code': fields.char('FedEx Shipment Code'),
    }


class FedExTrackingNumber(osv.osv):
    _name = 'fedex.tracking.number'
    _columns = {
	'name': fields.char('Name'),
	'picking_key': fields.char('Picking Key'),
	'tracking_number': fields.char('Tracking Number'),
    }



    def prepare_package_vals(self, shipment):
	picking_obj = self.pool.get('stock.picking')
	picking_ids = picking_obj.search(cr, uid, [('name', '=', shipment.picking_key)])
	if not picking_ids:
	    return False

	picking = picking_obj.browse(cr, uid, picking_ids[0])

	vals = {
		'name': shipment.tracking_number,
		'tracking_number': shipment.tracking_number,
		'picking': picking.id,
		'mage_package_state': 'pending',
		'sale': picking.sale.id,
		'cost': 0,
	}


    def sync_tracking_numbers(self, cr, uid, ids, context=None):
	tracking_ids = self.search(cr, uid, [], limit=100)
	package_obj = self.pool.get('stock.out.package')
	if not tracking_ids:
	    return True

	for tracking in self.browse(cr, uid, tracking_ids):
	    vals = self.prepare_package_vals(cr, uid, tracking)
	    if not vals:
		continue

	    package = package_obj.create(cr, uid, vals)
	    self.unlink(cr, uid, tracking.id)

	return True
