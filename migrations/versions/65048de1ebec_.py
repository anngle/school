"""empty message

Revision ID: 65048de1ebec
Revises: 25ecff1065c7
Create Date: 2018-09-15 20:31:59.141933

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '65048de1ebec'
down_revision = '25ecff1065c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schools', sa.Column('user', sa.Integer(), nullable=True))
    op.drop_constraint('schools_ibfk_1', 'schools', type_='foreignkey')
    op.create_foreign_key(None, 'schools', 'users', ['user'], ['id'])
    op.drop_column('schools', 'school')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schools', sa.Column('school', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'schools', type_='foreignkey')
    op.create_foreign_key('schools_ibfk_1', 'schools', 'users', ['school'], ['id'])
    op.drop_column('schools', 'user')
    # ### end Alembic commands ###
