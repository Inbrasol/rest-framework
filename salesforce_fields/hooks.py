from odoo import api, SUPERUSER_ID

def post_init_hook(cr, version):
    models = [
        'res_partner',
        'account_move',
        'account_move_line',
        'sale_order',
        'sale_order_line',
        'product_template',
        'crm_lead',
        'crm_lead_product'
    ]
    for model in models:
        cr.execute(f"""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name='{model}' AND column_name='skip_sync'
                ) THEN
                    ALTER TABLE {model} ADD COLUMN skip_sync BOOLEAN DEFAULT FALSE;
                END IF;
            END $$;
        """)