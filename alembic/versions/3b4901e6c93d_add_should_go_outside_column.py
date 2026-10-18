"""Add should_go_outside column

Revision ID: 3b4901e6c93d
Revises: 9273ae05b6da
Create Date: 2026-10-18 12:25:34.906753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b4901e6c93d'
down_revision: Union[str, Sequence[str], None] = '9273ae05b6da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Додаємо колонку як nullable=True
    op.add_column('air_quality', sa.Column('should_go_outside', sa.Boolean(), nullable=True))
    
    # Заповнюємо для вже існуючих записів за нашою формулою:
    # Виходити на вулицю варто (TRUE), якщо індекс EPA <= 2 І рівень пилу PM2.5 < 35.0
    op.execute("""
        UPDATE air_quality 
        SET should_go_outside = CASE 
            WHEN us_epa_index <= 2 AND pm2_5 < 35.0 THEN TRUE 
            ELSE FALSE 
        END
    """)
    
    # Етап 3: Встановлюємо обмеження NOT NULL
    op.alter_column('air_quality', 'should_go_outside', existing_type=sa.Boolean(), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    pass
