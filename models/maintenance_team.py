from odoo import models, fields

class MaintenanceTeam(models.Model):
    _name = 'gearguard.team'
    _description = 'Maintenance Team'

    name = fields.Char(string='Team Name', required=True)
    member_ids = fields.Many2many('res.users', string='Team Members')