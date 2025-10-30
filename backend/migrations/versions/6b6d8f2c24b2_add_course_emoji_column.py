"""Add emoji column to courses

Revision ID: 6b6d8f2c24b2
Revises: 89b6035fb115
Create Date: 2025-02-14 15:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b6d8f2c24b2'
down_revision = '89b6035fb115'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('courses', sa.Column('emoji', sa.String(length=16), nullable=True))
    op.execute("UPDATE courses SET emoji='📘' WHERE emoji IS NULL")


def downgrade():
    op.drop_column('courses', 'emoji')
