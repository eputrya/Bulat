"""fix

Revision ID: 4984e2480fa0
Revises: 8238a116fa33
Create Date: 2024-06-17 17:15:39.368651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4984e2480fa0'
down_revision = '8238a116fa33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tickets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('configuration', sa.Text(), nullable=False),
    sa.Column('img', sa.LargeBinary(), nullable=True),
    sa.Column('file', sa.LargeBinary(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.drop_table('tests')
    with op.batch_alter_table('configs', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'tickets', ['test_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('configs', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'tests', ['test_id'], ['id'])

    op.create_table('tests',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=80), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=False),
    sa.Column('configuration', sa.TEXT(), nullable=False),
    sa.Column('img', sa.BLOB(), nullable=True),
    sa.Column('file', sa.BLOB(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.drop_table('tickets')
    # ### end Alembic commands ###
