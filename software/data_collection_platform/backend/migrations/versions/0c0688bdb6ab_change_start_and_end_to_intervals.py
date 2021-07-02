"""change start and end to intervals

Revision ID: 0c0688bdb6ab
Revises: 40d7f87884c5
Create Date: 2021-07-02 16:13:54.401287

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0c0688bdb6ab'
down_revision = '40d7f87884c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('video', 'start',
               existing_type=postgresql.TIME(),
               type_=sa.Interval(),
               existing_nullable=True)
    op.alter_column('video', 'end',
               existing_type=postgresql.TIME(),
               type_=sa.Interval(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('video', 'end',
               existing_type=sa.Interval(),
               type_=postgresql.TIME(),
               existing_nullable=True)
    op.alter_column('video', 'start',
               existing_type=sa.Interval(),
               type_=postgresql.TIME(),
               existing_nullable=True)
    # ### end Alembic commands ###
