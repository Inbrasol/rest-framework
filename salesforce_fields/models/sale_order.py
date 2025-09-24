from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sf_id = fields.Char(string='Salesforce ID', index=True, unique=True)
    sf_integration_status = fields.Selection([
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('failed_final', 'Failed Final')
    ], string='Integration Status', default='pending', help="Status of the Salesforce integration")
    sf_integration_datetime = fields.Datetime(string='Integration Datetime')
    sf_integration_error = fields.Text(string='Integration Error')
    sf_retry_count = fields.Integer(string='Retry Count', default=0)
    sf_max_retries = fields.Integer(string='Max Retries', default=3)
    sf_last_sync_attempt = fields.Datetime(string='Last Sync Attempt')
    sf_error_code = fields.Char(string='Error Code')
    sf_owner_id = fields.Many2one('salesforce.user', string='Salesforce Owner')

    def _can_retry(self):
        """Verificar si el registro puede reintentar la sincronización"""
        self.ensure_one()
        return self.sf_retry_count < self.sf_max_retries and self.sf_integration_status == 'failed'
    
    def _increment_retry_count(self):
        """Incrementar el contador de reintentos"""
        self.ensure_one()
        self.sf_retry_count += 1
        self.sf_last_sync_attempt = fields.Datetime.now()
        
        if self.sf_retry_count >= self.sf_max_retries:
            self.sf_integration_status = 'failed_final'
            self._create_failure_report()
    
    def _create_failure_report(self):
        """Crear registro en el reporte de fallos definitivos"""
        self.ensure_one()
        self.env['salesforce.integration.failure.report'].create({
            'name': f"Sale Order {self.name} - Final Failure",
            'model_name': self._name,
            'record_id': self.id,
            'sf_id': self.sf_id or '',
            'error_message': self.sf_integration_error or 'Unknown error',
            'retry_count': self.sf_retry_count,
            'first_attempt': self.create_date,
            'last_attempt': self.sf_last_sync_attempt,
        })
    
    @api.model
    def get_priority_failed_records(self, limit=50):
        """Obtener registros fallidos ordenados por prioridad para reintentos"""
        domain = [
            ('sf_integration_status', '=', 'failed'),
            ('sf_retry_count', '<', 3)
        ]
        
        # Prioridad: sin reintentos > menos reintentos > más antiguos
        return self.search(domain, order='sf_retry_count asc, sf_last_sync_attempt asc', limit=limit)

    @api.model
    def default_get(self, fields_list):
        res = super(SaleOrder, self).default_get(fields_list)
        if 'sf_owner_id' in fields_list:
            opportunity = self.env.context.get('default_opportunity_id')
            if opportunity:
                opp = self.env['crm.lead'].browse(opportunity)
                if opp and opp.sf_owner_id:
                    res['sf_owner_id'] = opp.sf_owner_id.id
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    sf_id = fields.Char(string='Salesforce ID', index=True, unique=True)
    sf_integration_status = fields.Selection([
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('failed_final', 'Failed Final')
    ], string='Integration Status', default='pending', help="Status of the Salesforce integration")
    sf_integration_datetime = fields.Datetime(string='Integration Datetime')
    sf_integration_error = fields.Text(string='Integration Error')
    sf_retry_count = fields.Integer(string='Retry Count', default=0)
    sf_max_retries = fields.Integer(string='Max Retries', default=3)
    sf_last_sync_attempt = fields.Datetime(string='Last Sync Attempt')
    sf_error_code = fields.Char(string='Error Code')

    def _can_retry(self):
        """Verificar si el registro puede reintentar la sincronización"""
        self.ensure_one()
        return self.sf_retry_count < self.sf_max_retries and self.sf_integration_status == 'failed'
    
    def _increment_retry_count(self):
        """Incrementar el contador de reintentos"""
        self.ensure_one()
        self.sf_retry_count += 1
        self.sf_last_sync_attempt = fields.Datetime.now()
        
        if self.sf_retry_count >= self.sf_max_retries:
            self.sf_integration_status = 'failed_final'
            self._create_failure_report()
    
    def _create_failure_report(self):
        """Crear registro en el reporte de fallos definitivos"""
        self.ensure_one()
        self.env['salesforce.integration.failure.report'].create({
            'name': f"Sale Order Line {self.id} - Final Failure",
            'model_name': self._name,
            'record_id': self.id,
            'sf_id': self.sf_id or '',
            'error_message': self.sf_integration_error or 'Unknown error',
            'retry_count': self.sf_retry_count,
            'first_attempt': self.create_date,
            'last_attempt': self.sf_last_sync_attempt,
        })
    
    @api.model
    def get_priority_failed_records(self, limit=50):
        """Obtener registros fallidos ordenados por prioridad para reintentos"""
        domain = [
            ('sf_integration_status', '=', 'failed'),
            ('sf_retry_count', '<', 3)
        ]
        
        return self.search(domain, order='sf_retry_count asc, sf_last_sync_attempt asc', limit=limit)