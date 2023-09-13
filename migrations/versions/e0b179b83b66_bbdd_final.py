"""BBDD Final

Revision ID: e0b179b83b66
Revises: 7528cb641062
Create Date: 2023-09-13 12:20:45.998863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0b179b83b66'
down_revision = '7528cb641062'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friend_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('receiver_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('interest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('interest', sa.String(length=255), nullable=True),
    sa.Column('favorite_games', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('game_interests')
    op.drop_table('interests')
    op.drop_table('game')
    op.drop_table('gender_games')
    op.drop_table('profile_matches')
    op.drop_table('gender')
    with op.batch_alter_table('match', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id_1', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('user_id_2', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('connection_date', sa.Date(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['user_id_1'], ['id'])
        batch_op.create_foreign_key(None, 'user', ['user_id_2'], ['id'])

    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('social_media', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('rating', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('registration_date', sa.Date(), nullable=True))
        batch_op.alter_column('profile_picture',
               existing_type=sa.VARCHAR(length=250),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.drop_column('profile_interests')
        batch_op.drop_column('profile_groups')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_groups', sa.VARCHAR(length=250), nullable=True))
        batch_op.add_column(sa.Column('profile_interests', sa.VARCHAR(length=250), nullable=True))
        batch_op.alter_column('profile_picture',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=250),
               existing_nullable=True)
        batch_op.drop_column('registration_date')
        batch_op.drop_column('rating')
        batch_op.drop_column('social_media')
        batch_op.drop_column('description')

    with op.batch_alter_table('match', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('connection_date')
        batch_op.drop_column('user_id_2')
        batch_op.drop_column('user_id_1')

    op.create_table('gender',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('gender', sa.VARCHAR(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profile_matches',
    sa.Column('profile_id', sa.INTEGER(), nullable=False),
    sa.Column('match_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['match_id'], ['match.id'], ),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('profile_id', 'match_id')
    )
    op.create_table('gender_games',
    sa.Column('gender_id', sa.INTEGER(), nullable=False),
    sa.Column('game_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['gender_id'], ['gender.id'], ),
    sa.PrimaryKeyConstraint('gender_id', 'game_id')
    )
    op.create_table('game',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('interests',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('profile_id', sa.INTEGER(), nullable=False),
    sa.Column('game_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id', 'profile_id', 'game_id')
    )
    op.create_table('game_interests',
    sa.Column('game_id', sa.INTEGER(), nullable=False),
    sa.Column('interests_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['interests_id'], ['interests.id'], ),
    sa.PrimaryKeyConstraint('game_id', 'interests_id')
    )
    op.drop_table('interest')
    op.drop_table('friend_request')
    # ### end Alembic commands ###