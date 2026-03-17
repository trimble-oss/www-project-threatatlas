"""add_rbac_and_invitations

Revision ID: a1b2c3d4e5f6
Revises: 8e428cd957df
Create Date: 2026-02-14 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '8e428cd957df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create UserRole enum type explicitly
    op.execute("CREATE TYPE userrole AS ENUM ('admin', 'standard', 'read_only')")

    # Add role column to users (nullable first for data migration)
    op.add_column('users', sa.Column('role', postgresql.ENUM('admin', 'standard', 'read_only', name='userrole', create_type=False), nullable=True))

    # Add invited_by column to users
    op.add_column('users', sa.Column('invited_by', sa.Integer(), nullable=True))

    # Migrate existing users: superusers → admin, others → standard
    op.execute("UPDATE users SET role = 'admin' WHERE is_superuser = true")
    op.execute("UPDATE users SET role = 'standard' WHERE is_superuser = false OR is_superuser IS NULL")

    # Make role NOT NULL now that data is migrated
    op.alter_column('users', 'role', nullable=False)

    # Create foreign key for invited_by
    op.create_foreign_key('fk_users_invited_by', 'users', 'users', ['invited_by'], ['id'])

    # Create invitations table
    op.create_table('invitations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('token', sa.String(length=64), nullable=False),
        sa.Column('role', postgresql.ENUM('admin', 'standard', 'read_only', name='userrole', create_type=False), nullable=False),
        sa.Column('invited_by', sa.Integer(), nullable=False),
        sa.Column('is_accepted', sa.Boolean(), nullable=False),
        sa.Column('accepted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['invited_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_index(op.f('ix_invitations_email'), 'invitations', ['email'], unique=False)
    op.create_index(op.f('ix_invitations_id'), 'invitations', ['id'], unique=False)
    op.create_index(op.f('ix_invitations_token'), 'invitations', ['token'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop invitations table
    op.drop_index(op.f('ix_invitations_token'), table_name='invitations')
    op.drop_index(op.f('ix_invitations_id'), table_name='invitations')
    op.drop_index(op.f('ix_invitations_email'), table_name='invitations')
    op.drop_table('invitations')

    # Drop foreign key and columns from users
    op.drop_constraint('fk_users_invited_by', 'users', type_='foreignkey')
    op.drop_column('users', 'invited_by')
    op.drop_column('users', 'role')

    # Drop enum type
    sa.Enum(name='userrole').drop(op.get_bind())
