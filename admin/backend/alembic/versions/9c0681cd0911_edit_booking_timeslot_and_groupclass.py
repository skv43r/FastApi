"""Edit Booking Timeslot and GroupClass

Revision ID: 9c0681cd0911
Revises: 5c6cde528ca9
Create Date: 2024-12-06 12:45:31.943832

"""
from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c0681cd0911'
down_revision: Union[str, None] = '5c6cde528ca9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('booking', sa.Column('service_id', sa.Integer(), nullable=True))
    op.add_column('booking', sa.Column('class_id', sa.Integer(), nullable=True))
    op.add_column('booking', sa.Column('trainer_id', sa.Integer(), nullable=True))
    op.add_column('booking', sa.Column('timeslot_id', sa.Integer(), nullable=False))
    op.add_column('booking', sa.Column('user_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('booking', sa.Column('user_email', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('booking', sa.Column('user_phone', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.drop_column('booking', 'time')
    op.drop_column('booking', 'master')
    op.drop_column('booking', 'service')
    op.drop_constraint('groupclass_trainer_id_fkey', 'groupclass', type_='foreignkey')
    op.drop_column('groupclass', 'available_spots')
    op.drop_column('groupclass', 'trainer_id')
    op.add_column('timeslot', sa.Column('available_spots', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('timeslot', 'available_spots')
    op.add_column('groupclass', sa.Column('trainer_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('groupclass', sa.Column('available_spots', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('groupclass_trainer_id_fkey', 'groupclass', 'trainer', ['trainer_id'], ['id'])
    op.add_column('booking', sa.Column('service', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('booking', sa.Column('master', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('booking', sa.Column('time', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('booking', 'user_phone')
    op.drop_column('booking', 'user_email')
    op.drop_column('booking', 'user_name')
    op.drop_column('booking', 'timeslot_id')
    op.drop_column('booking', 'trainer_id')
    op.drop_column('booking', 'class_id')
    op.drop_column('booking', 'service_id')
    # ### end Alembic commands ###