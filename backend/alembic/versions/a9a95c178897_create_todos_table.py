"""create todos table

Revision ID: a9a95c178897
Revises: 
Create Date: 2024-03-21 16:10:09.832428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9a95c178897'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
     op.execute("""
     create table todos(
         id bigserial primary key,
         name text,
         completed boolean not null default false
     )
     """)

def downgrade():
     op.execute("drop table todos;")
