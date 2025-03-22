from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from games.domainmodel.model import Game, Publisher, Genre, User, Review


def test_game_orm(empty_session):
    game = Game(4, "The Sims 4")
    empty_session.add(game)
    empty_session.commit()

    game = Game(3, "The Sims 3")
    empty_session.add(game)
    empty_session.commit()

    # test saving
    rows = list(empty_session.execute('SELECT game_id, game_title FROM games'))
    assert rows == [(3, "The Sims 3"), (4, "The Sims 4")]

    # test querying
    test_game = empty_session.query(Game).filter(
        Game._Game__game_id == 4
    ).first()

    assert test_game is not None
    assert isinstance(test_game, Game)
    assert test_game.game_id == 4


def test_game_orm_invalid(empty_session):
    # test adding already existing game
    game = Game(4, "The Sims 4")
    empty_session.add(game)
    empty_session.commit()

    with pytest.raises(IntegrityError):
        game = Game(4, "The Sims 4")
        empty_session.add(game)
        empty_session.commit()


def test_publisher_orm(empty_session):
    publisher = Publisher("EA Sports")
    empty_session.add(publisher)
    empty_session.commit()

    publisher = Publisher("Nintendo")
    empty_session.add(publisher)
    empty_session.commit()

    # test saving
    rows = list(empty_session.execute('SELECT name FROM publishers'))
    assert rows == [("EA Sports",), ("Nintendo",)]

    # test querying
    test_publisher = empty_session.query(Publisher).filter(
        Publisher._Publisher__publisher_name == "EA Sports"
    ).first()

    assert test_publisher is not None
    assert isinstance(test_publisher, Publisher)
    assert test_publisher.publisher_name == "EA Sports"


def test_publisher_orm_invalid(empty_session):
    # test adding already existing publisher
    publisher = Publisher("EA Sports")
    empty_session.add(publisher)
    empty_session.commit()

    with pytest.raises(IntegrityError):
        publisher = Publisher("EA Sports")
        empty_session.add(publisher)
        empty_session.commit()


def test_genre_orm(empty_session):
    genre = Genre("Action")
    empty_session.add(genre)
    empty_session.commit()

    genre = Genre("Card Game")
    empty_session.add(genre)
    empty_session.commit()

    # test saving
    rows = list(empty_session.execute('SELECT genre_name FROM genres'))
    assert rows == [("Action",), ("Card Game",)]

    # test querying
    test_genre = empty_session.query(Genre).filter(
        Genre._Genre__genre_name == "Action"
    ).first()
    assert test_genre is not None
    assert isinstance(test_genre, Genre)
    assert test_genre.genre_name == "Action"


def test_genre_orm_invalid(empty_session):
    # test adding already existing genre
    genre = Genre("Action")
    empty_session.add(genre)
    empty_session.commit()

    with pytest.raises(IntegrityError):
        genre = Genre("Action")
        empty_session.add(genre)
        empty_session.commit()


def test_user_orm(empty_session):
    user = User("oliviarodrigo", "Passw0rd")
    empty_session.add(user)
    empty_session.commit()

    user = User("taylorswift", "Passw0rd")
    empty_session.add(user)
    empty_session.commit()

    # test saving
    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("oliviarodrigo", "Passw0rd"), ("taylorswift", "Passw0rd")]

    # test querying
    test_user = empty_session.query(User).filter(
        User._User__username == "oliviarodrigo"
    ).first()

    assert test_user is not None
    assert isinstance(test_user, User)
    assert test_user.username == "oliviarodrigo"


def test_user_orm_invalid(empty_session):
    # test adding already existing user
    user = User("oliviarodrigo", "Passw0rd")
    empty_session.add(user)
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("oliviarodrigo", "Passw0rd")
        empty_session.add(user)
        empty_session.commit()


def test_review_orm(empty_session):
    user = User("oliviarodrigo", "Passw0rd")
    game = Game(4, "The Sims 4")
    review = Review(user, game, 5, "Good", str(datetime.now()))

    empty_session.add(user)
    empty_session.add(game)
    empty_session.add(review)
    empty_session.commit()

    # test saving
    rows = list(empty_session.execute('SELECT user_name, game_id, rating, review_text FROM reviews'))
    assert rows == [("oliviarodrigo", 4, 5, "Good")]

    # test game-review mapping
    test_game = empty_session.query(Game).filter(
        Game._Game__game_id == 4
    ).first()
    assert test_game is not None
    assert test_game.reviews is not None
    assert review in test_game.reviews

    # test user-review mapping
    test_user = empty_session.query(User).filter(
        User._User__username == "oliviarodrigo"
    ).first()
    assert test_user is not None
    assert test_user.reviews is not None
    assert review in test_user.reviews


def test_game_publisher_mapping(empty_session):
    # test that the relationship has been mapped correctly
    publisher = Publisher("EA Sports")
    game = Game(4, "The Sims 4")
    game.publisher = publisher

    empty_session.add(publisher)
    empty_session.add(game)
    empty_session.commit()

    test_game = empty_session.query(Game).filter(
        Game._Game__game_id == 4
    ).first()

    assert test_game is not None
    assert test_game.publisher is not None
    assert test_game.publisher.publisher_name == "EA Sports"


def test_game_recommended_game_mapping(empty_session):
    # test that the relationship has been mapped correctly
    game = Game(4, "The Sims 4")
    game2 = Game(2, "The Sims 2")
    game3 = Game(3, "The Sims 3")

    game.add_recommended_game(game2)
    game.add_recommended_game(game3)

    empty_session.add(game)
    empty_session.add(game2)
    empty_session.add(game3)
    empty_session.commit()

    test_game = empty_session.query(Game).filter(
        Game._Game__game_id == 4
    ).first()

    assert test_game is not None
    assert test_game.recommended_games is not None
    assert len(test_game.recommended_games) == 2
    assert game2 in test_game.recommended_games
    assert game3 in test_game.recommended_games


def test_game_genre_mapping(empty_session):
    # test that the relationship has been mapped correctly
    game = Game(4, "The Sims 4")
    genre1 = Genre("Simulation")
    genre2 = Genre("Casual")

    game.add_genre(genre1)
    game.add_genre(genre2)

    empty_session.add(game)
    empty_session.add(genre1)
    empty_session.add(genre2)
    empty_session.commit()

    test_game = empty_session.query(Game).filter(
        Game._Game__game_id == 4
    ).first()

    assert test_game is not None
    assert test_game.genres is not None
    assert len(test_game.genres) == 2
    assert genre1 in test_game.genres
    assert genre2 in test_game.genres


def test_user_favourites_mapping(empty_session):
    # test that the relationship has been mapped correctly
    user = User("oliviarodrigo", "Passw0rd")
    game2 = Game(2, "The Sims 2")
    game3 = Game(3, "The Sims 3")

    # test adding favourite games
    user.add_favourite_game(game2)
    user.add_favourite_game(game3)

    empty_session.add(user)
    empty_session.add(game2)
    empty_session.add(game3)
    empty_session.commit()

    test_user = empty_session.query(User).filter(
        User._User__username == "oliviarodrigo"
    ).first()

    assert test_user is not None
    assert test_user.favourite_games is not None
    assert len(test_user.favourite_games) == 2
    assert game2 in test_user.favourite_games
    assert game3 in test_user.favourite_games

    # test removing favourite games
    user.remove_favourite_game(game2)
    empty_session.merge(user)
    empty_session.commit()

    test_user = empty_session.query(User).filter(
        User._User__username == "oliviarodrigo"
    ).first()

    assert test_user is not None
    assert test_user.favourite_games is not None
    assert len(test_user.favourite_games) == 1
    assert game2 not in test_user.favourite_games
    assert game3 in test_user.favourite_games