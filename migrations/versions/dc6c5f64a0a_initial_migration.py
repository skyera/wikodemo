"""initial migration

Revision ID: dc6c5f64a0a
Revises: None
Create Date: 2016-09-23 18:52:41.443471

"""

# revision identifiers, used by Alembic.
revision = 'dc6c5f64a0a'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('streams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('eid', sa.String(length=64), nullable=True),
    sa.Column('caption', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.Column('alias', sa.String(length=64), nullable=True),
    sa.Column('creation_time', sa.DateTime(), nullable=True),
    sa.Column('creator', sa.String(length=64), nullable=True),
    sa.Column('moderator', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('eid')
    )
    op.create_table('searchkeys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index('ix_roles_default', 'roles', ['default'], unique=False)
    op.create_table('searchkeytable',
    sa.Column('stream', sa.Integer(), nullable=True),
    sa.Column('searchkey', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['searchkey'], ['searchkeys.id'], ),
    sa.ForeignKeyConstraint(['stream'], ['streams.id'], )
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('location', sa.String(length=64), nullable=True),
    sa.Column('about_me', sa.Text(), nullable=True),
    sa.Column('member_since', sa.DateTime(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('avatar_hash', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pid', sa.String(length=64), nullable=True),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('body_html', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('stream_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.username'], ),
    sa.ForeignKeyConstraint(['stream_id'], ['streams.eid'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('pid')
    )
    op.create_index('ix_posts_timestamp', 'posts', ['timestamp'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_posts_timestamp', 'posts')
    op.drop_table('posts')
    op.drop_index('ix_users_username', 'users')
    op.drop_index('ix_users_email', 'users')
    op.drop_table('users')
    op.drop_table('searchkeytable')
    op.drop_index('ix_roles_default', 'roles')
    op.drop_table('roles')
    op.drop_table('searchkeys')
    op.drop_table('streams')
    ### end Alembic commands ###
