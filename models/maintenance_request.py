from odoo import models, fields, api

class MaintenanceRequest(models.Model):
    _name = 'gearguard.request'
    _description = 'Maintenance Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Subject', required=True) # [cite: 31]
    
    # Request Types [cite: 27]
    maintenance_type = fields.Selection([
        ('corrective', 'Corrective'),
        ('preventive', 'Preventive')
    ], string='Maintenance Type', default='corrective')

    # Workflow Stages [cite: 55]
    stage_id = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('repaired', 'Repaired'),
        ('scrap', 'Scrap')
    ], string='Stage', default='new', group_expand='_read_group_stage_ids', tracking=True)

    # Equipment Link [cite: 33]
    equipment_id = fields.Many2one('gearguard.equipment', string='Equipment', required=True)
    
    # Team & Technician
    team_id = fields.Many2one('gearguard.team', string='Team')
    user_id = fields.Many2one('res.users', string='Technician')

    # Scheduling & Duration [cite: 34-35]
    schedule_date = fields.Datetime(string='Scheduled Date')
    duration = fields.Float(string='Duration (Hours)')
    color = fields.Integer('Color Index') # For Kanban view

    # Auto-Fill Logic [cite: 40-41]
    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        if self.equipment_id:
            self.team_id = self.equipment_id.maintenance_team_id
            self.user_id = self.equipment_id.technician_id

    # Scrap Logic [cite: 76]
    def write(self, vals):
        if 'stage_id' in vals and vals['stage_id'] == 'scrap':
            for request in self:
                if request.equipment_id:
                    request.equipment_id.message_post(body="Equipment marked as Scrap due to maintenance request.")
        return super(MaintenanceRequest, self).write(vals)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """ Ensure all stages are visible in Kanban even if empty """
        return ['new', 'in_progress', 'repaired', 'scrap']