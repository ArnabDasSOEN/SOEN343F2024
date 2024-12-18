"""Add order_id column to notifications table

Revision ID: 0b6b9703d769
Revises: 
Create Date: 2024-11-14 11:21:54.736348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b6b9703d769'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'orders', ['order_id'], ['id'])

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'customers', ['customer_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('order_id')

    # ### end Alembic commands ###
