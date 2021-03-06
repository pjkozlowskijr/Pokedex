"""empty message

Revision ID: 279b29041d6f
Revises: 
Create Date: 2022-05-10 02:27:32.938188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '279b29041d6f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pokemon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('poke_id_num', sa.Integer(), nullable=True),
    sa.Column('height', sa.String(), nullable=True),
    sa.Column('weight', sa.String(), nullable=True),
    sa.Column('sprite', sa.String(), nullable=True),
    sa.Column('base_exp', sa.Integer(), nullable=True),
    sa.Column('ability', sa.String(), nullable=True),
    sa.Column('attack_base', sa.Integer(), nullable=True),
    sa.Column('hp_base', sa.Integer(), nullable=True),
    sa.Column('defense_base', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'user_poke', 'pokemon', ['poke_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_poke', type_='foreignkey')
    op.create_table('spatial_ref_sys',
    sa.Column('srid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('auth_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('auth_srid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('srtext', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.Column('proj4text', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.CheckConstraint('(srid > 0) AND (srid <= 998999)', name='spatial_ref_sys_srid_check'),
    sa.PrimaryKeyConstraint('srid', name='spatial_ref_sys_pkey')
    )
    op.drop_table('pokemon')
    # ### end Alembic commands ###
