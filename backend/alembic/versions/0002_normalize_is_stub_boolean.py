"""normalize papers.is_stub to boolean

Revision ID: 0002
Revises: 0001
Create Date: 2026-03-02
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Normalize any numeric/text legacy values before type conversion.
    op.execute(
        sa.text(
            """
            UPDATE papers
            SET is_stub = CASE
                WHEN is_stub IN (1, '1', 't', 'true', 'TRUE') THEN 1
                ELSE 0
            END
            """
        )
    )

    # Batch mode keeps this safe for SQLite by recreating the table as needed.
    with op.batch_alter_table("papers") as batch_op:
        batch_op.alter_column(
            "is_stub",
            existing_type=sa.Integer(),
            type_=sa.Boolean(),
            nullable=False,
            existing_nullable=False,
            server_default=sa.false(),
            existing_server_default=sa.text("0"),
        )


def downgrade() -> None:
    with op.batch_alter_table("papers") as batch_op:
        batch_op.alter_column(
            "is_stub",
            existing_type=sa.Boolean(),
            type_=sa.Integer(),
            nullable=False,
            existing_nullable=False,
            server_default=sa.text("0"),
            existing_server_default=sa.false(),
        )
