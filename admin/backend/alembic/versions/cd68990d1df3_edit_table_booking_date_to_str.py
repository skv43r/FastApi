"""Edit table booking date to str

Revision ID: cd68990d1df3
Revises: bcbf7f1ae69f
Create Date: 2024-11-29 12:38:01.780782

"""
from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd68990d1df3'
down_revision: Union[str, None] = 'bcbf7f1ae69f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('booking', 'dates',
               existing_type=sa.DATE(),
               type_=sqlmodel.sql.sqltypes.AutoString(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('booking', 'dates',
               existing_type=sqlmodel.sql.sqltypes.AutoString(),
               type_=sa.DATE(),
               existing_nullable=False)
    # ### end Alembic commands ###
