"""Edit model service

Revision ID: f2886a0c65de
Revises: 6317d58517f4
Create Date: 2024-12-09 15:25:57.146523

"""
from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2886a0c65de'
down_revision: Union[str, None] = '6317d58517f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_service_category', table_name='service')
    op.drop_column('service', 'category')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service', sa.Column('category', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_index('ix_service_category', 'service', ['category'], unique=False)
    # ### end Alembic commands ###
