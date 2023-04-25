"""empty message

Revision ID: ac2f1237e0fa
Revises: af14721b6d14
Create Date: 2023-04-25 00:55:50.372147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac2f1237e0fa'
down_revision = 'af14721b6d14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('answer_number', sa.Integer(), nullable=True),
    sa.Column('audio_URL', sa.String(length=120), nullable=True),
    sa.Column('audio_duration_seconds', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('audio')
    # ### end Alembic commands ###