"""add_risk_assessment_fields_to_diagram_threats

Revision ID: de84307a6882
Revises: 42d5e8ebdc8c
Create Date: 2026-02-13 15:33:03.732973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de84307a6882'
down_revision: Union[str, Sequence[str], None] = '42d5e8ebdc8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('diagram_threats', sa.Column('likelihood', sa.Integer(), nullable=True))
    op.add_column('diagram_threats', sa.Column('impact', sa.Integer(), nullable=True))
    op.add_column('diagram_threats', sa.Column('risk_score', sa.Integer(), nullable=True))
    op.add_column('diagram_threats', sa.Column('severity', sa.String(20), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('diagram_threats', 'severity')
    op.drop_column('diagram_threats', 'risk_score')
    op.drop_column('diagram_threats', 'impact')
    op.drop_column('diagram_threats', 'likelihood')
