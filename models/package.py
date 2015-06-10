from openerp.osv import osv, fields


class StockPackage(osv.osv):
    _inherit = 'stock.package'


    def sync_worldship_tracking_numbers(self, cr, uid, ids=None, context=None):

	trans_obj = self.pool.get('stock.transaction')
	tracking_obj = self.pool.get('worldship.tracking')

	tracking_ids = tracking_obj.search(cr, uid, [])
	if not tracking_ids:
	    return True

	tracking_objs = tracking_obj.browse(cr, uid, tracking_ids)
	trans_ids = []
	for tracking in tracking_objs:
	    trans_ids.append(int(tracking.package_id))

	    vals = {'package_state': 'complete',
		    'tracking_number': tracking.tracking_number,
		    'export_state': 'pending'
	    }

	    self.write(cr, uid, int(tracking.package_id), vals)
	    tracking_obj.unlink(cr, uid, tracking.id)

	    cr.commit()


	if len(trans_ids) < 1:
	    trans_ids.append(0)

	query = "SELECT DISTINCT transaction_id FROM stock_package WHERE id IN %s" % (tuple(trans_ids),)
	cr.execute(query)
	results = cr.fetchall()
	transaction_ids = [int(id[0]) for id in results]
	trans_objs = trans_obj.browse(cr, uid, transaction_ids)
	self.manifest_fulfillments(cr, uid, trans_objs)

	return True


