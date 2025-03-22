from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime, Text, Float,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from games.domainmodel.model import Game, Publisher, Genre, User, Review

metadata = MetaData()

publishers_table = Table(
    'publishers', metadata,
    Column('name', String(255), primary_key=True)  # nullable=False, unique=True)
)

genres_table = Table(
    'genres', metadata,
    Column('genre_name', String(64), primary_key=True, nullable=False)
)

games_table = Table(
    'games', metadata,
    Column('game_id', Integer, primary_key=True),
    Column('game_title', Text, nullable=False),
    Column('game_price', Float, nullable=True),
    Column('release_date', String(50), nullable=True),
    Column('game_description', String(255), nullable=True),
    Column('game_image_url', String(255), nullable=True),
    Column('game_website_url', String(255), nullable=True),
    Column('game_trailer_url', String(255), nullable=True),
    Column('publisher_name', ForeignKey('publishers.name')),
    Column('average_rating', Float, nullable=True, server_default='0'),
)

game_genres_table = Table(
    'game_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', Integer, ForeignKey('games.game_id')),
    Column('genre_name', ForeignKey('genres.genre_name'))
)

recommended_games_table = Table(
    'recommended_games', metadata,
    Column('game_id', Integer, ForeignKey('games.game_id'), primary_key=True),
    Column('recommended_game_id', Integer, ForeignKey('games.game_id'), primary_key=True)
)

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('review_id', Integer, primary_key=True, autoincrement=True),
    Column('review_text', String(255), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('user_name', ForeignKey('users.user_name')),
    Column('game_id', ForeignKey('games.game_id'))
)

favourites_table = Table(
    'favourites', metadata,
    Column('user_name', Integer, ForeignKey('users.user_name'), primary_key=True),
    Column('game_id', Integer, ForeignKey('games.game_id'), primary_key=True)
)


def map_model_to_tables():
    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name,
    })

    mapper(Game, games_table, properties={
        '_Game__game_id': games_table.c.game_id,
        '_Game__game_title': games_table.c.game_title,
        '_Game__price': games_table.c.game_price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.game_description,
        '_Game__image_url': games_table.c.game_image_url,
        '_Game__website_url': games_table.c.game_website_url,
        '_Game__trailer_url': games_table.c.game_trailer_url,
        '_Game__publisher': relationship(Publisher),
        '_Game__genres': relationship(Genre, secondary=game_genres_table),
        '_Game__reviews': relationship(Review, backref='_Review__game'),
        '_Game__average_rating': games_table.c.average_rating,
        '_Game__recommended_games': relationship(Game, secondary=recommended_games_table,
                                                 primaryjoin=(recommended_games_table.c.game_id == games_table.c.game_id),
                                                 secondaryjoin=(recommended_games_table.c.recommended_game_id == games_table.c.game_id))
    })

    mapper(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name
    })

    mapper(User, users_table, properties={
        '_User__username': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(Review, backref='_Review__user'),
        '_User__favourite_games': relationship(Game, secondary=favourites_table)
    })

    mapper(Review, reviews_table, properties={
        '_Review__comment': reviews_table.c.review_text,
        '_Review__rating': reviews_table.c.rating
    })
