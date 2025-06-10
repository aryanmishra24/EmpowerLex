"""Add user_id field to Feedback model

Revision ID: 57581413fe40
Revises: 71afacfb8163
Create Date: 2025-06-04 19:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '57581413fe40'
down_revision = '71afacfb8163'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('feedback') as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_feedback_user_id', 'users', ['user_id'], ['id'])

def downgrade():
    with op.batch_alter_table('feedback') as batch_op:
        batch_op.drop_constraint('fk_feedback_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')
