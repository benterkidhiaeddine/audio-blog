"""empty message

Revision ID: 1252715431d7
Revises: ac2f1237e0fa
Create Date: 2023-04-25 01:30:37.405826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1252715431d7'
down_revision = 'ac2f1237e0fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('audio', schema=None) as batch_op:
        batch_op.drop_column('audio_URL')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('audio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('audio_URL', sa.VARCHAR(length=120), nullable=True))

    # ### end Alembic commands ###