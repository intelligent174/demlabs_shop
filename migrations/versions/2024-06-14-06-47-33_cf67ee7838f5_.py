"""empty message

Revision ID: cf67ee7838f5
Revises: 7721f659a7d3
Create Date: 2024-06-14 06:47:33.617124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf67ee7838f5'
down_revision: Union[str, None] = '7721f659a7d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'product', ['title'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product', type_='unique')
    # ### end Alembic commands ###