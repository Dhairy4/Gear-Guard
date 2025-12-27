from odoo import models, fields, api


class GearGuardRequest(models.Model):
    _name = 'gearguard.request'
    _description = 'Maintenance Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Subject', required=True, tracking=True)
    request_date = fields.Date(
        string='Request Date',
        default=fields.Date.context_today
    )

    maintenance_type = fields.Selection(
        [
            ('corrective', 'Corrective'),
            ('preventive', 'Preventive')
        ],
        string='Type',
        default='corrective',
        tracking=True
    )

    schedule_date = fields.Datetime(string='Scheduled Date')
    duration = fields.Float(string='Duration (Hours)')

    equipment_id = fields.Many2one(
        'gearguard.equipment',
        string='Equipment',
        tracking=True
    )

    maintenance_team_id = fields.Many2one(
        'gearguard.team',
        string='Maintenance Team',
        tracking=True
    )

    user_id = fields.Many2one(
        'res.users',
        string='Technician',
        tracking=True
    )

    # ✅ REQUIRED for Kanban color coding
    color = fields.Integer(string='Color Index')

    stage_id = fields.Selection(
        [
            ('new', 'New'),
            ('in_progress', 'In Progress'),
            ('repaired', 'Repaired'),
            ('scrap', 'Scrap')
        ],
        string='Stage',
        default='new',
        group_expand='_expand_stages',
        tracking=True
    )

    @api.model
    def _expand_stages(self, states, domain, order):
        return [key for key, val in type(self).stage_id.selection]

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        if self.equipment_id and self.equipment_id.maintenance_team_id:
            self.maintenance_team_id = self.equipment_id.maintenance_team_id

    def write(self, vals):
        # Automation: If stage moved to "Scrap", post message in Equipment chatter
        if vals.get('stage_id') == 'scrap':
            for request in self:
                if request.equipment_id:
                    request.equipment_id.message_post(
                        body=f"Equipment has been scrapped due to Maintenance Request: {request.name}"
                    )

        return super(GearGuardRequest, self).write(vals)
