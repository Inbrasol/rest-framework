from odoo import api, SUPERUSER_ID

def pre_init_hook(env):
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
        env.execute(f"""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name='{model}' AND column_name='skip_sync'
                ) THEN
                    ALTER TABLE {model} ADD COLUMN skip_sync BOOLEAN DEFAULT FALSE;
                END IF;
                IF NOT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name='{model}' AND column_name='sf_integration_status'
                ) THEN
                    ALTER TABLE {model} ADD COLUMN sf_integration_status VARCHAR DEFAULT 'pending';
                END IF;
                IF NOT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name='{model}' AND column_name='sf_integration_datetime'
                ) THEN
                    ALTER TABLE {model} ADD COLUMN sf_integration_datetime TIMESTAMP;
                END IF;
                IF NOT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name='{model}' AND column_name='sf_integration_error'
                ) THEN
                    ALTER TABLE {model} ADD COLUMN sf_integration_error TEXT;
                END IF;
            END $$;
        """)