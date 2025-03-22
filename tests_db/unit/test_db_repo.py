from collections import Counter
from datetime import datetime
import random
import uuid

import pytest

from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import Game, Genre, Publisher, User, Review


def test_add_game(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # add game, test length
    game = Game(127, "Neo Culture Technology")
    test_repo.add_game(game)
    games = test_repo.get_all_games()
    assert len(games) == 878

    # add a non-Game object, test that it is not added
    not_game = 'game'
    test_repo.add_game(not_game)
    games = test_repo.get_all_games()
    assert len(games) == 878

    # test that it doesn't add an already existing game
    game_repeat = Game(127, "Neo Culture Technology")
    test_repo.add_game(game_repeat)
    games = test_repo.get_all_games()
    assert len(games) == 878


def test_add_publisher(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # add publisher, test length
    pub = Publisher("Neo Culture Technology")
    test_repo.add_publisher(pub)
    pubs = test_repo.get_all_publishers()
    assert len(pubs) == 799

    # add a non-Publisher object, test that it is not added
    not_pub = 'pub'
    test_repo.add_publisher(not_pub)
    pubs = test_repo.get_all_publishers()
    assert len(pubs) == 799

    # test that it doesn't add an already existing publisher
    pub_repeat = Publisher("Neo Culture Technology")
    test_repo.add_publisher(pub_repeat)
    pubs = test_repo.get_all_publishers()
    assert len(pubs) == 799


def test_add_genre(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # add genre, test length
    genre = Genre("Card Game")
    test_repo.add_genre(genre)
    genres = test_repo.get_all_genres()
    assert len(genres) == 25

    # add a non-Genre object, test that it is not added
    not_genre = 'genre'
    test_repo.add_genre(not_genre)
    genres = test_repo.get_all_genres()
    assert len(genres) == 25

    # test that it doesn't add an already existing genre
    genre_repeat = Genre("Card Game")
    test_repo.add_genre(genre_repeat)
    genres = test_repo.get_all_genres()
    assert len(genres) == 25


def test_add_user(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # add one User, test length
    user1 = User("user2", "Passw0rd")
    test_repo.add_user(user1)
    users = test_repo.get_all_users()
    assert len(users) == 1

    # add more users, test length
    user2 = User("user1", "Passw0rd")
    user3 = User("user3", "Passw0rd")
    test_repo.add_user(user2)
    test_repo.add_user(user3)
    users = test_repo.get_all_users()
    assert len(users) == 3

    # add a non-User object, test that it is not added
    not_user = 'user'
    test_repo.add_user(not_user)
    users = test_repo.get_all_users()
    assert len(users) == 3

    # test that it doesn't add an already existing user
    user_repeat = User("user1", "Passw0rd")
    test_repo.add_user(user_repeat)
    users = test_repo.get_all_users()
    assert len(users) == 3


def test_add_review(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    user1 = User("arianagrande", "Passw0rd")
    test_repo.add_user(user1)

    user = test_repo.get_user("arianagrande")
    game = test_repo.get_game(316260)
    rating = random.randint(1, 5)
    comment = (str(uuid.uuid4()))[0:100]
    current_datetime = str(datetime.now())

    user_review_count = len(user.reviews) + 1
    game_review_count = len(game.reviews) + 1

    # add a valid review, check it is present in both the User and Game objects
    review = Review(user, game, rating, comment, current_datetime)
    test_repo.add_review(review)
    assert len(user.reviews) == user_review_count
    assert len(game.reviews) == game_review_count
    assert review in user.reviews
    assert review in game.reviews


def test_get_game(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # get a game that exists in the repo
    game1 = Game(316260, "Disney Universe")
    test_game = test_repo.get_game(316260)
    assert test_game == game1

    # test for a game that does not exist in the repo
    test_game = test_repo.get_game(127)
    assert test_game is None

    # test for invalid inputs
    test_game = test_repo.get_game('string')
    assert test_game is None


def test_get_game_by_genre(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # test for a genre that exists in the repo
    genre1 = Genre("Action")
    action_games = test_repo.get_game_by_genre(genre1)
    assert len(action_games) == 380
    assert action_games[0] == Game(7940, "Call of DutyÂ® 4: Modern WarfareÂ®")

    # test for a genre that doesn't exist in the repo
    genre2 = Genre("Card Game")
    card_games = test_repo.get_game_by_genre(genre2)
    assert len(card_games) == 0

    # test for invalid input type
    card_games = test_repo.get_game_by_genre('Card Game')
    assert len(card_games) == 0


def test_get_game_by_publisher(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # test for a publisher that exists in the repo
    pub1 = Publisher("Activision")
    pub_games = test_repo.get_game_by_publisher(pub1)
    assert len(pub_games) == 1
    assert pub_games[0] == Game(7940, "Call of DutyÂ® 4: Modern WarfareÂ®")

    # test for a publisher that doesn't exist in the repo
    pub2 = Publisher("EA Sports")
    pub_games = test_repo.get_game_by_publisher(pub2)
    assert len(pub_games) == 0

    # test for invalid input type
    pub_games = test_repo.get_game_by_publisher('EA Sports')
    assert len(pub_games) == 0


def test_get_user(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # get a user that exists in the repo
    user1 = User("user01", "Passw0rd")
    test_repo.add_user(user1)
    test_user = test_repo.get_user("user01")
    assert test_user == user1

    # test for a user does not exist in the repo
    test_user = test_repo.get_user("user02")
    assert test_user is None


def test_get_all_games(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # test that it retrieves the correct number and type of object
    all_games = test_repo.get_all_games()
    assert len(all_games) == 877
    assert all(isinstance(game, Game) for game in all_games)


def test_get_all_genres(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # test that it retrieves the correct number and type of object
    all_genres = test_repo.get_all_genres()
    assert len(all_genres) == 24
    assert all(isinstance(genre, Genre) for genre in all_genres)


def test_get_all_publishers(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # test that it retrieves the correct number and type of object
    all_publishers = test_repo.get_all_publishers()
    assert len(all_publishers) == 798
    assert all(isinstance(publisher, Publisher) for publisher in all_publishers)


def test_get_all_users(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # test that it retrieves the correct number and type of object
    test_repo.add_user(User("arianagrande", "Passw0rd"))
    test_repo.add_user(User("taylorswift", "Passw0rd"))
    all_users = test_repo.get_all_users()
    assert len(all_users) == 2
    assert all(isinstance(user, User) for user in all_users)


def test_sort_games_by_date(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)
    sorted_games = test_repo.sort_games_by_date(test_repo.get_all_games())

    # test for the oldest game
    assert sorted_games[0] == Game(1995240, "Deer Journey")

    # test for the newest game
    assert sorted_games[-1] == Game(3010, "Xpand Rally")

    # test that games are sorted by release date
    for i in range(len(sorted_games) - 1):
        assert datetime.strptime(sorted_games[i].release_date, "%b %d, %Y") \
               >= datetime.strptime(sorted_games[i + 1].release_date, "%b %d, %Y")

    # test that list content remains the same
    assert len(sorted_games) == 877
    for game in sorted_games:
        assert game in test_repo.get_all_games()


def test_search_games_by_title(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # test an existing game title
    games = test_repo.search_games_by_title("Automobilista 2")
    assert len(games) == 1
    assert games[0] == Game(1066890, "Automobilista 2")

    # test a search string to return multiple games
    games = test_repo.search_games_by_title("ball")
    assert len(games) == 15

    # test that the search function is not case-sensitive
    games = test_repo.search_games_by_title("BALL")
    assert len(games) == 15

    # test that each game only occurs once in the list
    counts = Counter(games)
    assert all(count == 1 for count in counts.values())

    # test a search string that will not return any game
    games = test_repo.search_games_by_title("abcdefghijklmnopqrstuvwxyz")
    assert len(games) == 0


def test_search_games_by_genre(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # test an existing genre
    games = test_repo.search_games_by_genre("Action")
    assert len(games) == 380

    # test a search string that can involve multiple genres
    games = test_repo.search_games_by_genre("ac")
    assert len(games) == 430

    # test that the search function is not case-sensitive
    games = test_repo.search_games_by_genre("AC")
    assert len(games) == 430

    # test that each game only occurs once in the list
    counts = Counter(games)
    assert all(count == 1 for count in counts.values())

    # test a search string that will not return any game
    games = test_repo.search_games_by_genre("abcdefghijklmnopqrstuvwxyz")
    assert len(games) == 0


def test_search_games_by_publisher(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # test an existing publisher
    games = test_repo.search_games_by_publisher("Activision")
    assert len(games) == 1

    # test a search string that can involve multiple publishers
    games = test_repo.search_games_by_publisher("ac")
    assert len(games) == 60

    # test that the search function is not case-sensitive
    games = test_repo.search_games_by_publisher("Ac")
    assert len(games) == 60

    # test that each game only occurs once in the list
    counts = Counter(games)
    assert all(count == 1 for count in counts.values())

    # test a search string that will not return any game
    games = test_repo.search_games_by_publisher("abcdefghijklmnopqrstuvwxyz")
    assert len(games) == 0


def test_update_game(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # test that game is updated when a review is added
    user1 = User("arianagrande", "Passw0rd")
    test_repo.add_user(user1)

    user = test_repo.get_user("arianagrande")
    game = test_repo.get_game(316260)
    rating = 5
    comment = (str(uuid.uuid4()))[0:100]
    current_datetime = str(datetime.now())

    review = Review(user, game, rating, comment, current_datetime)
    test_repo.add_review(review)
    test_repo.update_game(game)

    test_game = test_repo.get_game(316260)
    assert len(test_game.reviews) == 1
    assert review in test_game.reviews


def test_update_user(session_factory):
    test_repo = SqlAlchemyRepository(session_factory)

    # test that user is updated when a review is added
    user1 = User("arianagrande", "Passw0rd")
    test_repo.add_user(user1)

    user = test_repo.get_user("arianagrande")
    game = test_repo.get_game(316260)
    rating = 5
    comment = (str(uuid.uuid4()))[0:100]
    current_datetime = str(datetime.now())

    review = Review(user, game, rating, comment, current_datetime)
    test_repo.add_review(review)
    test_repo.update_user(user)

    test_user = test_repo.get_user("arianagrande")
    assert len(test_user.reviews) == 1
    assert review in test_user.reviews

    # test that user is updated when a favourite game is added
    user.add_favourite_game(game)
    test_user = test_repo.get_user("arianagrande")
    assert len(test_user.favourite_games) == 1
    assert game in test_user.favourite_games

    # test that user is updated when a favourite game is removed
    user.remove_favourite_game(game)
    test_user = test_repo.get_user("arianagrande")
    assert len(test_user.favourite_games) == 0
    assert game not in test_user.favourite_games
