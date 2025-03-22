import random
import uuid
from collections import Counter
from datetime import datetime
from pathlib import Path

import pytest

from games.adapters.memory_repository import MemoryRepository
from games.adapters.repository_populate import populate
from games.authentication.services import add_user
from games.domainmodel.model import Game, Publisher, Genre, User, Review



def test_add_game():
    # add one Game, test length and that correct one is added
    test_repo = MemoryRepository()
    game1 = Game(127, "Neo Culture Technology")
    test_repo.add_game(game1)
    games = test_repo.get_all_games()
    assert len(games) == 1
    assert games[0] == game1

    # add more games, test length and that list is sorted by ID
    game2 = Game(4, "The Sims 4")
    game3 = Game(333, "The Sims 3")
    test_repo.add_game(game2)
    test_repo.add_game(game3)
    games = test_repo.get_all_games()
    assert len(games) == 3
    assert games[0] == game2
    assert games[1] == game1
    assert games[2] == game3

    # add a non-Game object, test that it is not added
    not_game = 'game'
    test_repo.add_game(not_game)
    games = test_repo.get_all_games()
    assert len(games) == 3

    # test that it doesn't add an already existing game
    game_repeat = Game(127, "Neo Culture Technology")
    test_repo.add_game(game_repeat)
    games = test_repo.get_all_games()
    assert len(games) == 3


def test_add_publisher():
    # add one Publisher, test length and that correct one is added
    test_repo = MemoryRepository()
    pub1 = Publisher("Nintendo")
    test_repo.add_publisher(pub1)
    pubs = test_repo.get_all_publishers()
    assert len(pubs) == 1
    assert pubs[0] == pub1

    # add more Publishers, test length and that list is sorted by name
    pub2 = Publisher("EA Sports")
    pub3 = Publisher("Warner Bros")
    test_repo.add_publisher(pub2)
    test_repo.add_publisher(pub3)
    pubs = test_repo.get_all_publishers()
    assert len(pubs) == 3
    assert pubs[0] == pub2
    assert pubs[1] == pub1
    assert pubs[2] == pub3

    # add a non-Publisher object, test that it is not added
    not_pub = 'pub'
    test_repo.add_publisher(not_pub)
    pubs = test_repo.get_all_publishers()
    assert len(pubs) == 3

    # test that it doesn't add an already existing publisher
    pub_repeat = Publisher("EA Sports")
    test_repo.add_publisher(pub_repeat)
    pubs = test_repo.get_all_publishers()
    assert len(pubs) == 3


def test_add_genre():
    # add one Genre, test length and that correct one is added
    test_repo = MemoryRepository()
    genre1 = Genre("Card Game")
    test_repo.add_genre(genre1)
    genres = test_repo.get_all_genres()
    assert len(genres) == 1
    assert genres[0] == genre1

    # add more genres, test length and that list is sorted by name
    genre2 = Genre("Adventure")
    genre3 = Genre("Simulation")
    test_repo.add_genre(genre2)
    test_repo.add_genre(genre3)
    genres = test_repo.get_all_genres()
    assert len(genres) == 3
    assert genres[0] == genre2
    assert genres[1] == genre1
    assert genres[2] == genre3

    # add a non-Genre object, test that it is not added
    not_genre = 'genre'
    test_repo.add_genre(not_genre)
    genres = test_repo.get_all_genres()
    assert len(genres) == 3

    # test that it doesn't add an already existing genre
    genre_repeat = Genre("Adventure")
    test_repo.add_genre(genre_repeat)
    genres = test_repo.get_all_genres()
    assert len(genres) == 3


def test_get_game():
    # get a game that exists in the repo
    test_repo = MemoryRepository()
    game1 = Game(127, "Neo Culture Technology")
    test_repo.add_game(game1)
    test_game = test_repo.get_game(127)
    assert test_game == game1

    # test for a game that exists but is not in the repo
    game2 = Game(1, "The Sims 4")
    test_game = test_repo.get_game(2)
    assert test_game is None

    # test for a game that does not exist
    test_game = test_repo.get_game(3)
    assert test_game is None

    # test for invalid inputs
    test_game = test_repo.get_game('string')
    assert test_game is None


def test_get_game_by_genre():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

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


def test_get_game_by_publisher():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

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


def test_get_all_games():
    # test if there are no games
    test_repo = MemoryRepository()
    games = test_repo.get_all_games()
    assert len(games) == 0

    # test if there is one game
    game1 = Game(127, "Neo Culture Technology")
    test_repo.add_game(game1)
    games = test_repo.get_all_games()
    assert len(games) == 1

    # test if there are multiple games
    game2 = Game(4, "The Sims 4")
    game3 = Game(333, "The Sims 3")
    test_repo.add_game(game2)
    test_repo.add_game(game3)
    games = test_repo.get_all_games()
    assert len(games) == 3

    # test that it doesn't retrieve a game that isn't in the list
    game4 = Game(100, "The Sims FreePlay")
    games = test_repo.get_all_games()
    assert len(games) == 3
    assert game4 not in games


def test_get_all_genres():
    # test if there are no genres
    test_repo = MemoryRepository()
    genres = test_repo.get_all_genres()
    assert len(genres) == 0

    # test if there is one genre
    genre1 = Genre("Card Game")
    test_repo.add_genre(genre1)
    genres = test_repo.get_all_genres()
    assert len(genres) == 1

    # test if there are multiple genres
    genre2 = Genre("Adventure")
    genre3 = Genre("Simulation")
    test_repo.add_genre(genre2)
    test_repo.add_genre(genre3)
    genres = test_repo.get_all_genres()
    assert len(genres) == 3

    # test that it doesn't retrieve a genre that isn't in the list
    genre4 = Genre("Board Game")
    genres = test_repo.get_all_genres()
    assert len(genres) == 3
    assert genre4 not in genres


def test_get_all_publishers():
    # test if there are no publishers
    test_repo = MemoryRepository()
    pubs = test_repo.get_all_publishers()
    assert len(pubs) == 0

    # test if there is one publisher
    pub1 = Publisher("Nintendo")
    test_repo.add_publisher(pub1)
    pubs = test_repo.get_all_publishers()
    assert len(pubs) == 1

    # test if there are multiple publishers
    pub2 = Publisher("EA Sports")
    pub3 = Publisher("Rokstarr")
    test_repo.add_publisher(pub2)
    test_repo.add_publisher(pub3)
    pubs = test_repo.get_all_publishers()
    assert len(pubs) == 3

    # test that it doesn't retrieve a publisher that isn't in the list
    pub4 = Publisher("Sega")
    pubs = test_repo.get_all_publishers()
    assert len(pubs) == 3
    assert pub4 not in pubs


def test_sort_games_by_date():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)
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


def test_search_games_by_title():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

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


def test_search_games_by_genre():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

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


def test_search_games_by_publisher():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

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


def test_add_review():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

    user1 = User("baekhyunbyun", "Passw0rd")
    test_repo.add_user(user1)

    user = test_repo.get_user("baekhyunbyun")
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

    # attempt to add a review that already is present in either object
    test_repo.add_review(review)
    assert len(user.reviews) == user_review_count
    assert len(game.reviews) == game_review_count

    # test invalid inputs
    not_review = 'user'
    test_repo.add_review(not_review)
    assert not_review not in user.reviews
    assert not_review not in game.reviews


def test_add_user():
    # add one User, test length and that correct one is added
    test_repo = MemoryRepository()
    user1 = User("user2", "Passw0rd")
    test_repo.add_user(user1)
    users = test_repo.get_all_users()
    assert len(users) == 1
    assert users[0] == user1

    # add more users, test length and that list is sorted by username
    user2 = User("user1", "Passw0rd")
    user3 = User("user3", "Passw0rd")
    test_repo.add_user(user2)
    test_repo.add_user(user3)
    users = test_repo.get_all_users()
    assert len(users) == 3
    assert users[0] == user2
    assert users[1] == user1
    assert users[2] == user3

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


def test_get_user():
    # get a user that exists in the repo
    test_repo = MemoryRepository()
    user1 = User("user01", "Passw0rd")
    test_repo.add_user(user1)
    test_user = test_repo.get_user("user01")
    assert test_user == user1

    # test for a user that exists but is not in the repo
    user2 = User("user02", "Passw0rd")
    test_user = test_repo.get_user("user02")
    assert test_user is None

    # test for a user that does not exist
    test_user = test_repo.get_user("user03")
    assert test_user is None


def test_get_all_users():
    # test if there are no users
    test_repo = MemoryRepository()
    users = test_repo.get_all_users()
    assert len(users) == 0

    # test if there is one user
    user1 = User("userone", "Passw0rd")
    test_repo.add_user(user1)
    users = test_repo.get_all_users()
    assert len(users) == 1

    # test if there are multiple users
    user2 = User("usertwo", "Passw0rd")
    user3 = User("userthree", "Passw0rd")
    test_repo.add_user(user2)
    test_repo.add_user(user3)
    users = test_repo.get_all_users()
    assert len(users) == 3

    # test that it doesn't retrieve a user that isn't in the list
    user4 = User("userfour", "Passw0rd")
    users = test_repo.get_all_users()
    assert len(users) == 3
    assert user4 not in users
