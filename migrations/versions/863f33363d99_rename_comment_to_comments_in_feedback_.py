"""Rename comment to comments in Feedback model

Revision ID: 863f33363d99
Revises: 57581413fe40
Create Date: 2025-06-05 00:52:45.786497

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '863f33363d99'
down_revision: Union[str, None] = '57581413fe40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feedback', sa.Column('comments', sa.Text(), nullable=True))
    op.drop_column('feedback', 'comment')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feedback', sa.Column('comment', sa.TEXT(), nullable=True))
    op.drop_column('feedback', 'comments')
    # ### end Alembic commands ###
