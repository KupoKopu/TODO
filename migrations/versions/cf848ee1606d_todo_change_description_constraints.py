"""todo change description constraints

Revision ID: cf848ee1606d
Revises: 156bbd9fadf5
Create Date: 2024-07-14 18:01:50.115091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf848ee1606d'
down_revision = '156bbd9fadf5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('to_do', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
        batch_op.drop_index('ix_to_do_description')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('to_do', schema=None) as batch_op:
        batch_op.create_index('ix_to_do_description', ['description'], unique=False)
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)

    # ### end Alembic commands ###