from odoo import models, fields,api, re


class MyProject(models.Model):
    _inherit = ['project.project']

    x_prefix = fields.Char(
        string="Prefix",
        size=3,
        help="Prefix maksimal 3 karakter"
    )
    x_ada_git = fields.Boolean(string="Ada Git?", help="Centang jika proyek memiliki repository Git.")

    @api.model
    def create(self, vals):
        """Mengisi x_prefix dengan 3 huruf pertama dari nama proyek, dengan aturan khusus."""
        if 'name' in vals and not vals.get('x_prefix'):
            name = vals['name'].strip()  # Hilangkan spasi di awal & akhir
            prefix = name[:3]  # Ambil 3 karakter pertama

            # Jika karakter ketiga adalah spasi, ambil karakter keempat sebagai gantinya
            if len(prefix) > 2 and prefix[2] == " ":
                if len(name) > 3:
                    prefix = name[:2] + name[3]  # Ambil 2 huruf pertama + huruf keempat
                else:
                    prefix = name[:2]  # Jika kurang dari 4 karakter, ambil 2 pertama saja

            # Jika karakter keempat bukan huruf, hanya gunakan 2 huruf pertama
            if len(prefix) > 2 and not re.match(r'[A-Za-z]', prefix[2]):
                prefix = prefix[:2]

            vals['x_prefix'] = prefix.upper()  # Ubah ke huruf besar

        return super(MyProject, self).create(vals)

    @api.constrains('x_prefix')
    def _check_x_prefix_length(self):
        """Pastikan x_prefix tidak lebih dari 3 karakter."""
        for record in self:
            if record.x_prefix and len(record.x_prefix) > 3:
                raise models.ValidationError("Prefix tidak boleh lebih dari 3 karakter.")

    def write(self, vals):
        """Setiap kali x_prefix diubah, pastikan selalu Uppercase & maksimal 3 karakter"""
        if 'x_prefix' in vals:
            vals['x_prefix'] = vals['x_prefix'][:3].upper()  # Maks 3 karakter & UPPERCASE

        return super(MyProject, self).write(vals)
