"""empty message

Revision ID: 7ccea71744a0
Revises: 
Create Date: 2021-01-18 22:51:59.303616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ccea71744a0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job', sa.Column('date_posted', sa.DateTime(), nullable=True))
    op.add_column('residence', sa.Column('date_posted', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('residence', 'date_posted')
    op.drop_column('job', 'date_posted')
    # ### end Alembic commands ###