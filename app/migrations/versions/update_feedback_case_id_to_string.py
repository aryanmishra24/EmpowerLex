"""update feedback case_id to string

Revision ID: update_feedback_case_id_to_string
Revises: 71afacfb8163
Create Date: 2024-03-21 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'update_feedback_case_id_to_string'
down_revision = '71afacfb8163'
branch_labels = None
depends_on = None

def upgrade():
    # Drop the existing foreign key constraint
    op.drop_constraint('feedback_case_id_fkey', 'feedback', type_='foreignkey')
    
    # Alter the column type
    op.alter_column('feedback', 'case_id',
                    existing_type=sa.Integer(),
                    type_=sa.String(36),
                    existing_nullable=True)
    
    # Add the new foreign key constraint
    op.create_foreign_key('feedback_case_id_fkey', 'feedback', 'cases',
                         ['case_id'], ['case_id'])

def downgrade():
    # Drop the existing foreign key constraint
    op.drop_constraint('feedback_case_id_fkey', 'feedback', type_='foreignkey')
    
    # Alter the column type back to Integer
    op.alter_column('feedback', 'case_id',
                    existing_type=sa.String(36),
                    type_=sa.Integer(),
                    existing_nullable=True)
    
    # Add the old foreign key constraint
    op.create_foreign_key('feedback_case_id_fkey', 'feedback', 'cases',
                         ['case_id'], ['id']) 