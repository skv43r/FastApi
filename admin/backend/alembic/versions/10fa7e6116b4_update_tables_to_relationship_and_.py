"""Update tables to relationship and create table TimeSlot

Revision ID: 10fa7e6116b4
Revises: ae6457d83f2c
Create Date: 2024-11-28 11:50:19.678763

"""
from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10fa7e6116b4'
down_revision: Union[str, None] = 'ae6457d83f2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('timeslot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('trainer_id', sa.Integer(), nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('available', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['service_id'], ['service.id'], ),
    sa.ForeignKeyConstraint(['trainer_id'], ['trainer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('timeslot')
    # ### end Alembic commands ###
