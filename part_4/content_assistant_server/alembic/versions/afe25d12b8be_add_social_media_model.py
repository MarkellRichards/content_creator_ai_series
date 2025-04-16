"""Add social media model

Revision ID: afe25d12b8be
Revises: 590234b3400b
Create Date: 2025-04-05 03:36:08.416476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afe25d12b8be'
down_revision: Union[str, None] = '590234b3400b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('social_media_posts',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('guid', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=True),
    sa.Column('platform_type', sa.Enum('LINKEDIN', 'FACEBOOK', 'TWITTER', 'INSTAGRAM', 'OTHER', name='platformtype'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('workflow_guid', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['workflow_guid'], ['workflows.guid'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('guid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('social_media_posts')
    # ### end Alembic commands ###
