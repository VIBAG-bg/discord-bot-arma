"""rename status to recruit_status

Revision ID: 405531f51299
Revises: 764b00f658fd
Create Date: 2025-11-17 ..
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # на будущее, пусть будет


revision: str = "405531f51299"
down_revision: Union[str, Sequence[str], None] = "764b00f658fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # переименуем колонку status -> recruit_status
    op.alter_column("users", "status", new_column_name="recruit_status")
    # на всякий пожарный — если вдруг там есть NULL
    op.execute(
        "UPDATE users SET recruit_status = 'pending' WHERE recruit_status IS NULL"
    )


def downgrade() -> None:
    # откатим обратно
    op.alter_column("users", "recruit_status", new_column_name="status")
