"""add_threat_modeling_models

Revision ID: ad8d0fe1c1de
Revises: 4c0a12f2173f
Create Date: 2026-02-17 13:06:44.084406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad8d0fe1c1de'
down_revision: Union[str, Sequence[str], None] = '4c0a12f2173f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create everything using raw SQL to avoid SQLAlchemy enum issues
    connection = op.get_bind()

    # Create modelstatus enum (only if it doesn't exist)
    connection.execute(sa.text("""
        DO $$ BEGIN
            CREATE TYPE modelstatus AS ENUM ('in_progress', 'completed', 'archived');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """))

    # Create models table using raw SQL
    connection.execute(sa.text("""
        CREATE TABLE models (
            id SERIAL PRIMARY KEY,
            diagram_id INTEGER NOT NULL REFERENCES diagrams(id) ON DELETE CASCADE,
            framework_id INTEGER NOT NULL REFERENCES frameworks(id),
            name VARCHAR(255) NOT NULL,
            description TEXT,
            status modelstatus NOT NULL DEFAULT 'in_progress',
            created_by INTEGER REFERENCES users(id),
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            completed_at TIMESTAMP WITH TIME ZONE
        )
    """))

    # Create index
    connection.execute(sa.text("CREATE INDEX ix_models_id ON models (id)"))

    # Add model_id column to diagram_threats (nullable initially for data migration)
    op.add_column('diagram_threats', sa.Column('model_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_diagram_threats_model_id'), 'diagram_threats', ['model_id'], unique=False)

    # Add model_id column to diagram_mitigations (nullable initially for data migration)
    op.add_column('diagram_mitigations', sa.Column('model_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_diagram_mitigations_model_id'), 'diagram_mitigations', ['model_id'], unique=False)

    # Migrate existing data: Create default models for each diagram/framework combination
    # This SQL will:
    # 1. Find unique diagram_id + framework_id combinations from existing threats/mitigations
    # 2. Create a model for each combination
    # 3. Link existing threats and mitigations to the created model

    # Create models for existing diagram/framework combinations (from threats)
    connection.execute(sa.text("""
        INSERT INTO models (diagram_id, framework_id, name, status, created_by, created_at)
        SELECT DISTINCT
            dt.diagram_id,
            t.framework_id,
            f.name || ' Analysis',
            'in_progress'::modelstatus,
            d.created_by,
            NOW()
        FROM diagram_threats dt
        JOIN threats t ON dt.threat_id = t.id
        JOIN frameworks f ON t.framework_id = f.id
        JOIN diagrams d ON dt.diagram_id = d.id
        WHERE NOT EXISTS (
            SELECT 1 FROM models m
            WHERE m.diagram_id = dt.diagram_id
            AND m.framework_id = t.framework_id
        )
    """))

    # Create models for existing diagram/framework combinations (from mitigations not yet covered)
    connection.execute(sa.text("""
        INSERT INTO models (diagram_id, framework_id, name, status, created_by, created_at)
        SELECT DISTINCT
            dm.diagram_id,
            m.framework_id,
            f.name || ' Analysis',
            'in_progress'::modelstatus,
            d.created_by,
            NOW()
        FROM diagram_mitigations dm
        JOIN mitigations m ON dm.mitigation_id = m.id
        JOIN frameworks f ON m.framework_id = f.id
        JOIN diagrams d ON dm.diagram_id = d.id
        WHERE NOT EXISTS (
            SELECT 1 FROM models mo
            WHERE mo.diagram_id = dm.diagram_id
            AND mo.framework_id = m.framework_id
        )
    """))

    # Update diagram_threats to link to the appropriate model
    connection.execute(sa.text("""
        UPDATE diagram_threats dt
        SET model_id = (
            SELECT mo.id
            FROM models mo
            JOIN threats t ON dt.threat_id = t.id
            WHERE mo.diagram_id = dt.diagram_id
            AND mo.framework_id = t.framework_id
            LIMIT 1
        )
    """))

    # Update diagram_mitigations to link to the appropriate model
    connection.execute(sa.text("""
        UPDATE diagram_mitigations dm
        SET model_id = (
            SELECT mo.id
            FROM models mo
            JOIN mitigations m ON dm.mitigation_id = m.id
            WHERE mo.diagram_id = dm.diagram_id
            AND mo.framework_id = m.framework_id
            LIMIT 1
        )
    """))

    # Now make model_id NOT NULL and add foreign key constraints
    op.alter_column('diagram_threats', 'model_id', nullable=False)
    op.create_foreign_key('fk_diagram_threats_model_id', 'diagram_threats', 'models', ['model_id'], ['id'], ondelete='CASCADE')

    op.alter_column('diagram_mitigations', 'model_id', nullable=False)
    op.create_foreign_key('fk_diagram_mitigations_model_id', 'diagram_mitigations', 'models', ['model_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    # Remove foreign keys
    op.drop_constraint('fk_diagram_mitigations_model_id', 'diagram_mitigations', type_='foreignkey')
    op.drop_constraint('fk_diagram_threats_model_id', 'diagram_threats', type_='foreignkey')

    # Drop columns
    op.drop_index(op.f('ix_diagram_mitigations_model_id'), table_name='diagram_mitigations')
    op.drop_column('diagram_mitigations', 'model_id')

    op.drop_index(op.f('ix_diagram_threats_model_id'), table_name='diagram_threats')
    op.drop_column('diagram_threats', 'model_id')

    # Drop models table
    op.drop_index(op.f('ix_models_id'), table_name='models')
    op.drop_table('models')

    # Drop enum
    sa.Enum('in_progress', 'completed', 'archived', name='modelstatus').drop(op.get_bind())
