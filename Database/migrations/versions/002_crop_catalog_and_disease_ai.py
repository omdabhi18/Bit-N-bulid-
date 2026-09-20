"""002_crop_catalog_and_disease_ai

Revision ID: 002_crop_catalog_and_disease_ai
Revises: 001_initial_schema
Create Date: 2026-09-20 14:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002_crop_catalog_and_disease_ai'
down_revision: Union[str, None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add catalog support columns to crops table
    with op.batch_alter_table('crops') as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('name_gujarati', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('category', sa.String(length=100), server_default='Cash Crop', nullable=True))
        batch_op.add_column(sa.Column('scientific_name', sa.String(length=150), nullable=True))
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), server_default=sa.true(), nullable=True))
        batch_op.add_column(sa.Column('disease_ai_supported', sa.Boolean(), server_default=sa.false(), nullable=True))
        batch_op.add_column(sa.Column('stage', sa.String(length=100), server_default='Vegetative', nullable=True))
        batch_op.add_column(sa.Column('field_name', sa.String(length=100), server_default='Field A', nullable=True))

        batch_op.create_index('ix_crops_name', ['name'])
        batch_op.create_index('ix_crops_name_gujarati', ['name_gujarati'])
        batch_op.create_index('ix_crops_category', ['category'])
        batch_op.create_index('ix_crops_disease_ai_supported', ['disease_ai_supported'])

    # 2. Add crop_id reference column to disease_analyses table
    with op.batch_alter_table('disease_analyses') as batch_op:
        batch_op.add_column(sa.Column('crop_id', sa.String(length=50), nullable=True))
        batch_op.create_index('ix_disease_analyses_crop_id', ['crop_id'])


def downgrade() -> None:
    with op.batch_alter_table('disease_analyses') as batch_op:
        batch_op.drop_index('ix_disease_analyses_crop_id')
        batch_op.drop_column('crop_id')

    with op.batch_alter_table('crops') as batch_op:
        batch_op.drop_index('ix_crops_disease_ai_supported')
        batch_op.drop_index('ix_crops_category')
        batch_op.drop_index('ix_crops_name_gujarati')
        batch_op.drop_index('ix_crops_name')
        batch_op.drop_column('field_name')
        batch_op.drop_column('stage')
        batch_op.drop_column('disease_ai_supported')
        batch_op.drop_column('is_active')
        batch_op.drop_column('scientific_name')
        batch_op.drop_column('category')
        batch_op.drop_column('name_gujarati')
        batch_op.drop_column('name')
