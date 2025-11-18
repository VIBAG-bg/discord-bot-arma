"""rename status to recruit_status

Revision ID: 405531f51299
Revises: 764b00f658fd
Create Date: 2025-11-17 11:20:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "405531f51299"
down_revision: Union[str, Sequence[str], None] = "764b00f658fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Переименовываем колонку status -> recruit_status
    op.alter_column(
        "users",
        "status",
        new_column_name="recruit_status",
        existing_type=sa.String(length=20),
        existing_nullable=False,
    )

    # На всякий случай: если вдруг где-то были NULL – сделаем "new"
    op.execute(
        "UPDATE users SET recruit_status = 'new' "
        "WHERE recruit_status IS NULL"
    )


def downgrade() -> None:
    # Откат: вернуть имя recruit_status -> status
    op.alter_column(
        "users",
        "recruit_status",
        new_column_name="status",
        existing_type=sa.String(length=20),
        existing_nullable=False,
    )
