"""empty message

Revision ID: f28df111fff9
Revises: 
Create Date: 2020-02-24 23:59:09.667043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f28df111fff9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('datetime',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('depart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('departname', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('meetingroom',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('roomname', sa.String(length=50), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=True),
    sa.Column('telephone', sa.String(length=20), nullable=True),
    sa.Column('departId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['departId'], ['depart.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bookedroom',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('roomid', sa.Integer(), nullable=True),
    sa.Column('bookedtime', sa.String(length=30), nullable=False),
    sa.ForeignKeyConstraint(['roomid'], ['meetingroom.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bookedroom')
    op.drop_table('user')
    op.drop_table('meetingroom')
    op.drop_table('depart')
    op.drop_table('datetime')
    # ### end Alembic commands ###