"""empty message

Revision ID: 7553a07cde88
Revises: 
Create Date: 2019-04-21 18:39:53.008615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7553a07cde88'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('urls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('url', sa.String(length=512), nullable=False),
    sa.Column('canonical_rel', sa.String(length=512), nullable=True),
    sa.Column('title', sa.String(length=512), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('images_json', sa.Text(), nullable=True),
    sa.Column('category', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('urls')
    # ### end Alembic commands ###
