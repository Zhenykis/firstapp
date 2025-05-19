"""fix_is_banned_default

Revision ID: c212df88c6cf
Revises: 6b34acc3752e
Create Date: 2025-05-13 22:47:53.255400

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c212df88c6cf"
down_revision: Union[str, None] = "6b34acc3752e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
