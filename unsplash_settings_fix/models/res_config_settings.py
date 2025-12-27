from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    unsplash_access_key = fields.Char(
        string="Unsplash Access Key"
    )
