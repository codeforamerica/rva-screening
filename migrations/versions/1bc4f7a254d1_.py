"""empty message

Revision ID: 1bc4f7a254d1
Revises: 455d4e8cc28
Create Date: 2015-10-05 17:09:15.166090

"""

# revision identifiers, used by Alembic.
revision = '1bc4f7a254d1'
down_revision = '455d4e8cc28'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('patient', sa.Column('spouse_years_at_current_employer', sa.String(length=32), nullable=True))
    op.add_column('patient', sa.Column('years_at_current_employer', sa.String(length=32), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('patient', 'years_at_current_employer')
    op.drop_column('patient', 'spouse_years_at_current_employer')
    ### end Alembic commands ###
