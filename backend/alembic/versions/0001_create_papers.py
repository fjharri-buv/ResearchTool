"""create papers

Revision ID: 0001_create_papers
Revises:
Create Date: 2026-03-02
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_create_papers"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "papers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("doi", sa.String(length=255), nullable=True, unique=True),
        sa.Column("title", sa.String(length=1024), nullable=False),
        sa.Column("year", sa.Integer(), nullable=True),
        sa.Column("venue", sa.String(length=512), nullable=True),
        sa.Column("abstract", sa.Text(), nullable=True),
        sa.Column("url", sa.String(length=1024), nullable=True),
        sa.Column("pdf_path", sa.String(length=1024), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="to_read"),
        sa.Column("is_stub", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("added_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_papers_id", "papers", ["id"])
    op.create_index("ix_papers_doi", "papers", ["doi"])
    op.create_index("ix_papers_title", "papers", ["title"])
    op.create_index("ix_papers_year", "papers", ["year"])
    op.create_index("ix_papers_status", "papers", ["status"])


def downgrade() -> None:
    op.drop_index("ix_papers_status", table_name="papers")
    op.drop_index("ix_papers_year", table_name="papers")
    op.drop_index("ix_papers_title", table_name="papers")
    op.drop_index("ix_papers_doi", table_name="papers")
    op.drop_index("ix_papers_id", table_name="papers")
    op.drop_table("papers")
