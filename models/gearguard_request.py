from odoo import models, fields, api

class MaintenanceRequest(models.Model):
    _name = 'gearguard.request'
    _description = 'Maintenance Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Subject', required=True)
    request_date = fields.Date(string='Request Date', default=fields.Date.context_today)
    maintenance_type = fields.Selection([
        ('corrective', 'Corrective'),
        ('preventive', 'Preventive')
    ], string='Type', default='corrective')
    
    schedule_date = fields.Datetime(string='Scheduled Date')
    duration = fields.Float(string='Duration (Hours)')
    
    equipment_id = fields.Many2one('gearguard.equipment', string='Equipment')
    maintenance_team_id = fields.Many2one('gearguard.team', string='Maintenance Team')
    user_id = fields.Many2one('res.users', string='Technician')
    
    stage_id = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('repaired', 'Repaired'),
        ('scrap', 'Scrap')
    ], string='Stage', default='new', group_expand='_expand_stages', tracking=True)

    @api.model
    def _expand_stages(self, states, domain, order):
        return [key for key, val in type(self).stage_id.selection]

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        if self.equipment_id:
            if self.equipment_id.maintenance_team_id:
                self.maintenance_team_id = self.equipment_id.maintenance_team_id
            # Auto-fill technician logic? 
            # Requirement: "automatically fill the 'Maintenance Team' and 'Technician' based on the equipment's default settings."
            # Equipment has "Default Maintenance Team". It doesn't strictly have a "Default Technician".
            # I'll assume if the specific technician is implied by team or separate field. 
            # Looking at equipment model... it has 'employee_id' (Owner) but not default technician.
            # I will just map maintenance team. 
            # Or maybe member_ids of team? But that's many.
            # I'll stick to just mapping what exists.
            
    def write(self, vals):
        # Automation 2: If stage moved to "Scrap", post message in Equipment chatter.
        if 'stage_id' in vals and vals['stage_id'] == 'scrap':
            for request in self:
                if request.equipment_id:
                    request.equipment_id.message_post(
                        body=f"Equipment has been scrapped due to Maintenance Request: {request.name}"
                    )
        return super(MaintenanceRequest, self).write(vals)
