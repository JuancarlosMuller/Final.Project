"""BD Genero 2

Revision ID: 2966873f4427
Revises: 063fd9240de9
Create Date: 2023-09-14 13:34:44.201764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2966873f4427'
down_revision = '063fd9240de9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('genero', schema=None) as batch_op:
        batch_op.add_column(sa.Column('genero', sa.String(length=255), nullable=True))
        batch_op.drop_column('interest')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('genero', schema=None) as batch_op:
        batch_op.add_column(sa.Column('interest', sa.VARCHAR(length=255), nullable=True))
        batch_op.drop_column('genero')

    # ### end Alembic commands ###