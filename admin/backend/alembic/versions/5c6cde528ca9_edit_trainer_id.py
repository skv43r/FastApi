"""Edit trainer_id

Revision ID: 5c6cde528ca9
Revises: 250064e0b11d
Create Date: 2024-12-05 15:31:02.072120

"""
from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c6cde528ca9'
down_revision: Union[str, None] = '250064e0b11d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'groupclass', 'trainer', ['trainer_id'], ['id'])
    op.alter_column('trainergroup', 'group_class_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('trainergroup', 'group_class_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint(None, 'groupclass', type_='foreignkey')
    # ### end Alembic commands ###
