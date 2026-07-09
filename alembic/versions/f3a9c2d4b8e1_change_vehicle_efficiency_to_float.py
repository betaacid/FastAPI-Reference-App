"""change vehicle efficiency to float

Revision ID: f3a9c2d4b8e1
Revises: e7b1f1b1b1b4
Create Date: 2026-07-09

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "f3a9c2d4b8e1"
down_revision: Union[str, None] = "e7b1f1b1b1b4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "star_wars_vehicles",
        "efficiency",
        existing_type=sa.Integer(),
        type_=sa.Float(),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "star_wars_vehicles",
        "efficiency",
        existing_type=sa.Float(),
        type_=sa.Integer(),
        existing_nullable=True,
    )
