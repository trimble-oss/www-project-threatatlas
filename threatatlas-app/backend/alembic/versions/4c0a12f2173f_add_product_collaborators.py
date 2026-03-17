"""add_product_collaborators

Revision ID: 4c0a12f2173f
Revises: a1b2c3d4e5f6
Create Date: 2026-02-16 16:16:38.959492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '4c0a12f2173f'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create collaborator role enum if it doesn't exist
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE collaboratorrole AS ENUM ('owner', 'editor', 'viewer');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Create product_collaborators table
    op.create_table(
        'product_collaborators',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role', postgresql.ENUM('owner', 'editor', 'viewer', name='collaboratorrole', create_type=False), nullable=False),
        sa.Column('added_by', sa.Integer(), nullable=False),
        sa.Column('added_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['added_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('product_id', 'user_id', name='unique_product_user')
    )
    op.create_index(op.f('ix_product_collaborators_id'), 'product_collaborators', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_product_collaborators_id'), table_name='product_collaborators')
    op.drop_table('product_collaborators')
    op.execute("DROP TYPE collaboratorrole")
