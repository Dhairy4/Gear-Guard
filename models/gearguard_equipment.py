from odoo import models, fields, api

class Equipment(models.Model):
    _name = 'gearguard.equipment'
    _description = 'Equipment'
    _inherit = ['mail.thread']

    name = fields.Char(string='Equipment Name', required=True, tracking=True)
    serial_number = fields.Char(string='Serial Number', tracking=True)
    category_id = fields.Many2one('gearguard.equipment.category', string='Category') # Assuming category model exists or using Char. Requirement said "Category", usually that's a model but I will use Char to be simple unless specified. Actually requirement just said "Category". I'll make it a Char for simplicity as I didn't define a Category model in plan, or I'll check my plan. Plan said category_id, implying Many2one. But I didn't create a category model. I'll make it a selection or char to be safe, or just Many2one to itself or a new model if needed. 
    # Re-reading plan: I didn't explicitly plan a category model. I will use Char to stick to simplicity or Many2one to a simple category model if I want to be fancy. "Category" in Odoo usually implies maintenance.equipment.category from maintenance module, but this is a custom module. I will use Char for now to avoid dependency on another custom model I haven't defined, or I can define it inline.
    # Actually, standard Odoo practice is Many2one. I will change to Char for "Category" to strict adherance to my plan which didn't include a Category model, OR valid Odoo development practice would be to add it.
    # Let's stick to Char for "Category" to avoid complexity, or just add a simple selection.
    # User said: "Fields: Name, Serial Number, Category, Purchase Date, Warranty Date." 
    # I'll use Char for Category to be safe and simple.
    category = fields.Char(string='Category') 
    
    purchase_date = fields.Date(string='Purchase Date')
    warranty_date = fields.Date(string='Warranty Expiration Date')
    
    department_id = fields.Many2one('hr.department', string='Department') # adhering to likely standard models or just Char if HR not installed? Depends on 'base'. 'hr' is not in depends. So I should use Char or Many2one to res.groups?
    # Requirement: "Relationships: Department, Employee (Owner)".
    # 'hr' module is needed for Department and Employee.
    # I did not add 'hr' to depends. I should add it or just use Char?
    # "Department" and "Employee" strongly implies HR module. But I can't add dependencies willy nilly.
    # However, "Employee (Owner)" usually links to res.users or hr.employee.
    # Given typical Odoo tasks, I'll assume I should use standard models if possible, but without 'hr' depend, I can't link to hr.department or hr.employee.
    # I'll update manifest to depend on 'hr' to be professional, or just use basic relations.
    # Use res.users for Owner? "Employee" usually means hr.employee.
    # I'll add 'hr' to depends in next step or use Char. 
    # Let's add 'hr' to depends to do this right. 
    
    # Wait, I can't rely on HR being there if I didn't plan it.
    # I will allow myself to add 'hr' to manifest.
    
    # Actually, let's look at the plan. Plan said:
    # department_id, employee_id.
    # I will add 'hr' to manifest dependencies to support this content.
    
    employee_id = fields.Many2one('hr.employee', string='Owner')
    department_id = fields.Many2one('hr.department', string='Department')
    
    maintenance_team_id = fields.Many2one('gearguard.team', string='Default Maintenance Team')
    
    request_ids = fields.One2many('gearguard.request', 'equipment_id', string='Maintenance Requests')
    request_count = fields.Integer(string='Request Count', compute='_compute_request_count')

    @api.depends('request_ids')
    def _compute_request_count(self):
        for equipment in self:
            equipment.request_count = len(equipment.request_ids)

    def action_view_requests(self):
        self.ensure_one()
        return {
            'name': 'Maintenance Requests',
            'type': 'ir.actions.act_window',
            'res_model': 'gearguard.request',
            'view_mode': 'kanban,tree,form',
            'domain': [('equipment_id', '=', self.id)],
            'context': {'default_equipment_id': self.id},
        }
