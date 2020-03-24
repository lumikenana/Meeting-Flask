"""empty message

Revision ID: 933322ebb8c0
Revises: f28df111fff9
Create Date: 2020-02-26 16:37:03.776981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '933322ebb8c0'
down_revision = 'f28df111fff9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('features',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('featurename', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('menu', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'menu')
    op.drop_table('features')
    # ### end Alembic commands ###
