"""TokenConstraint

Revision ID: 787c36ff6dc8
Revises: f26e4fdd9706
Create Date: 2020-08-26 00:50:05.068815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '787c36ff6dc8'
down_revision = 'f26e4fdd9706'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('hodler_address_token_unique', 'hodlers', ['address', 'token_name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('hodler_address_token_unique', 'hodlers', type_='unique')
    # ### end Alembic commands ###