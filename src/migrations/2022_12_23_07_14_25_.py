"""empty message

Revision ID: 553460c5c09c
Revises: 
Create Date: 2022-12-23 07:14:25.638365+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '553460c5c09c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='ID'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Date and time of creation'),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Date and time of last update'),
    sa.Column('deleted_at', sa.DateTime(), nullable=True, comment='Date and time of logic deletion'),
    sa.Column('is_deleted', sa.Boolean(), nullable=False, comment='Is object marked as deleted'),
    sa.Column('email', sa.String(length=255), nullable=False, comment='Email'),
    sa.Column('password', sa.String(length=255), nullable=False, comment='Password'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('links',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='ID'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Date and time of creation'),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Date and time of last update'),
    sa.Column('deleted_at', sa.DateTime(), nullable=True, comment='Date and time of logic deletion'),
    sa.Column('is_deleted', sa.Boolean(), nullable=False, comment='Is object marked as deleted'),
    sa.Column('original_url', sa.String(length=255), nullable=False, comment='Original URL'),
    sa.Column('link_type', sa.String(length=32), nullable=False, comment='Link type'),
    sa.Column('user_id', sa.Integer(), nullable=True, comment='User'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('follows',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='ID'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Date and time of creation'),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Date and time of last update'),
    sa.Column('deleted_at', sa.DateTime(), nullable=True, comment='Date and time of logic deletion'),
    sa.Column('is_deleted', sa.Boolean(), nullable=False, comment='Is object marked as deleted'),
    sa.Column('link_id', sa.Integer(), nullable=False, comment='Link ID'),
    sa.Column('user_id', sa.Integer(), nullable=True, comment='User ID'),
    sa.ForeignKeyConstraint(['link_id'], ['links.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('follows')
    op.drop_table('links')
    op.drop_table('users')
    # ### end Alembic commands ###
