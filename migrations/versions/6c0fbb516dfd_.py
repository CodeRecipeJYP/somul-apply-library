"""empty message

Revision ID: 6c0fbb516dfd
Revises: ad3c95a8a551
Create Date: 2018-04-11 23:34:31.356913

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6c0fbb516dfd'
down_revision = 'ad3c95a8a551'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('speaker',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('phone', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=30), nullable=False),
    sa.Column('is_email_verified', sa.Boolean(), nullable=True),
    sa.Column('email_sended_at', sa.DateTime(), nullable=True),
    sa.Column('session_time', sa.Enum('first', 'second', name='sessionenum'), nullable=False),
    sa.Column('library_id', mysql.INTEGER(display_width=11, unsigned=True), nullable=False),
    sa.ForeignKeyConstraint(['library_id'], ['Libraries.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.alter_column('Libraries', 'name',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True)
    op.drop_index('name', table_name='Libraries')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('name', 'Libraries', ['name'], unique=True)
    op.alter_column('Libraries', 'name',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False)
    op.drop_table('speaker')
    # ### end Alembic commands ###
