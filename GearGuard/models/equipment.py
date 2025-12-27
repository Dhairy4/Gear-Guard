from odoo import models, fields, api

class Equipment(models.Model):
    _name = 'gearguard.equipment'
    _description = 'Equipment / Asset'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Equipment Name', required=True)
    serial_number = fields.Char(string='Serial Number')
    category_id = fields.Many2one('gearguard.equipment.category', string='Category') # Optional grouping
    
    # Ownership & Location [cite: 11, 18]
    department_id = fields.Many2one('hr.department', string='Department')
    employee_id = fields.Many2one('res.users', string='Employee/Owner')
    location = fields.Char(string='Physical Location')

    # Technical Details [cite: 17]
    purchase_date = fields.Date(string='Purchase Date')
    warranty_date = fields.Date(string='Warranty Expiry')

    # Default Maintenance Team [cite: 12]
    maintenance_team_id = fields.Many2one('gearguard.team', string='Maintenance Team')
    technician_id = fields.Many2one('res.users', string='Assigned Technician')

    # Smart Button Logic [cite: 73]
    maintenance_count = fields.Integer(compute='_compute_maintenance_count', string="Maintenance Count")

    def _compute_maintenance_count(self):
        for record in self:
            record.maintenance_count = self.env['gearguard.request'].search_count([('equipment_id', '=', record.id)])

    def action_view_maintenance(self):
        """ Smart button action to view related requests [cite: 72] """
        return {
            'name': 'Maintenance Requests',
            'type': 'ir.actions.act_window',
            'res_model': 'gearguard.request',
            'view_mode': 'tree,form',
            'domain': [('equipment_id', '=', self.id)],
            'context': {'default_equipment_id': self.id},
        }