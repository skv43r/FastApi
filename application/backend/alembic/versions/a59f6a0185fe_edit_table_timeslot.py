"""Edit table TimeSlot

Revision ID: a59f6a0185fe
Revises: f658d7cf4a34
Create Date: 2024-11-28 16:22:12.307375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a59f6a0185fe'
down_revision: Union[str, None] = 'f658d7cf4a34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('timeslot', sa.Column('dates', sa.Date(), nullable=False))
    op.drop_column('timeslot', 'date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('timeslot', sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('timeslot', 'dates')
    # ### end Alembic commands ###
