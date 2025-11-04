"""all

Revision ID: bd7a932b7ff9
Revises: 77693b4be7db
Create Date: 2025-11-04 12:46:49.904332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bd7a932b7ff9'
down_revision: Union[str, Sequence[str], None] = '77693b4be7db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add driver_id column
    op.add_column(
        "order",
        sa.Column("driver_id", postgresql.UUID(as_uuid=True), nullable=True)
    )

    # Add foreign key constraint
    op.create_foreign_key(
        constraint_name="fk_order_driver_id_driver",
        source_table="order",
        referent_table="driver",
        local_cols=["driver_id"],
        remote_cols=["id"],
        ondelete="SET NULL"
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop foreign key constraint (safe even if missing)
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    fkeys = [fk["name"] for fk in inspector.get_foreign_keys("order")]
    if "fk_order_driver_id_driver" in fkeys:
        op.drop_constraint("fk_order_driver_id_driver", "order", type_="foreignkey")

    # Drop the column if it exists
    columns = [col["name"] for col in inspector.get_columns("order")]
    if "driver_id" in columns:
        op.drop_column("order", "driver_id")
