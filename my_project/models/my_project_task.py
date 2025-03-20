from odoo import models, fields,api


class MyProjectTask(models.Model):
    _inherit = ['project.task']

    x_task_id = fields.Char(
        string="Task ID",
        index=True,
        readonly=True,  # Agar tidak bisa diedit manual
        copy=False,  # Tidak disalin saat duplikasi
        help="Auto-generated task ID using project prefix."
    )
    x_git_branch_type = fields.Selection(
        [
            ('', 'others'),
            ('feature', 'Feature'),
            ('hotfix', 'Hotfix'),
            ('bugfix', 'Bugfix'),
            ('patch', 'Patch')
        ], string="Git Branch Type", default=""
    )
    x_git_checkout_branch = fields.Char(
        string="Git Checkout Branch",
        compute="_compute_git_branch", store=True)
    
    x_ada_git = fields.Boolean(
        string="Ada Git?",
        related='project_id.x_ada_git',  # Ambil langsung dari project
        store=True
    )

    @api.model
    def create(self, vals):
        """Saat membuat task baru, otomatis set x_task_id dengan format PREFIX-0001"""
        if 'project_id' in vals:
            project = self.env['project.project'].browse(vals['project_id'])

            if project.x_prefix:  # Pastikan proyek memiliki x_prefix
                prefix = project.x_prefix.upper()

                # Hitung jumlah task yang sudah ada dalam proyek ini
                existing_tasks = self.search([('project_id', '=', project.id), ('x_task_id', 'ilike', f'{prefix}-%')])
                task_count = len(existing_tasks) + 1  # Nomor berikutnya

                # Format nomor: ITD-0001, ITS-0030
                vals['x_task_id'] = f"{prefix}-{task_count:04d}"

        return super(MyProjectTask, self).create(vals)

    @api.depends("x_git_branch_type", "x_task_id")
    def _compute_git_branch(self):
        """ Generate git checkout command based on x_git_branch_type and x_task_id """
        for rec in self:
            if rec.x_git_branch_type and rec.x_task_id:
                rec.x_git_checkout_branch = f"git checkout -b {rec.x_git_branch_type}/{rec.x_task_id}"
