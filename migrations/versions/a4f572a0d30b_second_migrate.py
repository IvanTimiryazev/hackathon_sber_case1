"""second migrate

Revision ID: a4f572a0d30b
Revises: e4c6b485f77e
Create Date: 2023-04-15 22:22:08.979243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4f572a0d30b'
down_revision = 'e4c6b485f77e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('users', 'surname',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.drop_column('users', 'patronymic')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('patronymic', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.alter_column('users', 'surname',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###
