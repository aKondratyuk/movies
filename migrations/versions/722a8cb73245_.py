"""empty message

Revision ID: 722a8cb73245
Revises: 1b43c19ab8fe
Create Date: 2020-02-07 15:43:47.601523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '722a8cb73245'
down_revision = '1b43c19ab8fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genre',
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.Column('genre_name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('genre_id'),
    sa.UniqueConstraint('genre_name')
    )
    op.create_table('role',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('role_name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('role_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=2000), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.role_id'], ),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('genre')
    # ### end Alembic commands ###
