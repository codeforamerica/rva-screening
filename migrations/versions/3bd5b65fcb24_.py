"""empty message

Revision ID: 3bd5b65fcb24
Revises: 65f28fd897d
Create Date: 2015-09-23 15:27:56.520868

"""

# revision identifiers, used by Alembic.
revision = '3bd5b65fcb24'
down_revision = '65f28fd897d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('referral_permission', sa.Column('to_service_id', sa.Integer(), nullable=True))
    op.drop_constraint(u'referral_permission_to_servide_id_fkey', 'referral_permission', type_='foreignkey')
    op.create_foreign_key('fk_last_modified_by_id', 'referral_permission', 'app_user', ['last_modified_by_id'], ['id'])
    op.create_foreign_key(None, 'referral_permission', 'service', ['to_service_id'], ['id'])
    op.create_foreign_key('fk_created_by_id', 'referral_permission', 'app_user', ['created_by_id'], ['id'])
    op.drop_column('referral_permission', 'to_servide_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('referral_permission', sa.Column('to_servide_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint('fk_created_by_id', 'referral_permission', type_='foreignkey')
    op.drop_constraint(None, 'referral_permission', type_='foreignkey')
    op.drop_constraint('fk_last_modified_by_id', 'referral_permission', type_='foreignkey')
    op.create_foreign_key(u'referral_permission_to_servide_id_fkey', 'referral_permission', 'service', ['to_servide_id'], ['id'])
    op.drop_column('referral_permission', 'to_service_id')
    ### end Alembic commands ###