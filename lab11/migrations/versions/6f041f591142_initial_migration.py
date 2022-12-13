"""Initial migration.

Revision ID: 6f041f591142
Revises: 
Create Date: 2022-12-11 14:33:21.285924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f041f591142'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('person',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=False),
    sa.Column('subject', sa.String(length=30), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('image', sa.String(length=20), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('about_me', sa.String(length=120), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=2048), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.Column('priority', sa.Enum('1', '2', '3', name='priority'), nullable=True),
    sa.Column('progress', sa.Enum('1', '2', '3', name='progress'), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('text', sa.String(length=2048), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task_user',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task_user')
    op.drop_table('comment')
    op.drop_table('task')
    op.drop_table('user')
    op.drop_table('person')
    op.drop_table('category')
    # ### end Alembic commands ###
