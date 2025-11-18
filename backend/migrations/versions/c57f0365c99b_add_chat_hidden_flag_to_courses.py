"""Add chat_hidden_for_students flag to courses

Revision ID: c57f0365c99b
Revises: 6b6d8f2c24b2
Create Date: 2025-02-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c57f0365c99b'
down_revision = '6b6d8f2c24b2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'courses',
        sa.Column(
            'chat_hidden_for_students',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('0')
        )
    )
    op.execute("UPDATE courses SET chat_hidden_for_students = 0 WHERE chat_hidden_for_students IS NULL")
    op.alter_column('courses', 'chat_hidden_for_students', server_default=None)


def downgrade():
    op.drop_column('courses', 'chat_hidden_for_students')
