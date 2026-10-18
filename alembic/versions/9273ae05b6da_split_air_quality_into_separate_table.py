"""Split air quality into separate table

Revision ID: 9273ae05b6da
Revises: 850b1ad96fe0
Create Date: 2026-10-18 12:21:32.313864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9273ae05b6da'
down_revision: Union[str, Sequence[str], None] = '850b1ad96fe0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Створюємо нову таблицю air_quality
    op.create_table(
        'air_quality',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('weather_id', sa.Integer(), nullable=False),
        sa.Column('carbon_monoxide', sa.Float(), nullable=True),
        sa.Column('ozone', sa.Float(), nullable=True),
        sa.Column('nitrogen_dioxide', sa.Float(), nullable=True),
        sa.Column('sulphur_dioxide', sa.Float(), nullable=True),
        sa.Column('pm2_5', sa.Float(), nullable=True),
        sa.Column('pm10', sa.Float(), nullable=True),
        sa.Column('us_epa_index', sa.Integer(), nullable=True),
        sa.Column('gb_defra_index', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['weather_id'], ['weather_reports.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('weather_id')
    )

    # Переносимо існуючі дані зі старої таблиці в нову
    op.execute("""
        INSERT INTO air_quality (
            weather_id, carbon_monoxide, ozone, nitrogen_dioxide, 
            sulphur_dioxide, pm2_5, pm10, us_epa_index, gb_defra_index
        )
        SELECT 
            id, air_quality_carbon_monoxide, air_quality_ozone, air_quality_nitrogen_dioxide,
            air_quality_sulphur_dioxide, air_quality_pm2_5, air_quality_pm10, 
            air_quality_us_epa_index, air_quality_gb_defra_index
        FROM weather_reports
    """)

    # 3. Видаляємо старі колонки з weather_reports
    op.drop_column('weather_reports', 'air_quality_carbon_monoxide')
    op.drop_column('weather_reports', 'air_quality_ozone')
    op.drop_column('weather_reports', 'air_quality_nitrogen_dioxide')
    op.drop_column('weather_reports', 'air_quality_sulphur_dioxide')
    op.drop_column('weather_reports', 'air_quality_pm2_5')
    op.drop_column('weather_reports', 'air_quality_pm10')
    op.drop_column('weather_reports', 'air_quality_us_epa_index')
    op.drop_column('weather_reports', 'air_quality_gb_defra_index')


def downgrade() -> None:
    """Downgrade schema."""
    pass
