"""empty message

Revision ID: 20414cd1ebbf
Revises: 620f827577c4
Create Date: 2021-01-26 02:30:43.779734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20414cd1ebbf'
down_revision = '620f827577c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.String(length=255), nullable=True),
    sa.Column('data', sa.LargeBinary(), nullable=True),
    sa.Column('expiry', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('session_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sessions')
    # ### end Alembic commands ###
