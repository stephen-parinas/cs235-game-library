import random
import uuid
from collections import Counter
from datetime import datetime
from pathlib import Path

import pytest

from games.adapters.memory_repository import MemoryRepository
from games.adapters.repository_populate import populate
from games.allgames.services import get_all_games, pagination
from games.authentication.services import user_to_dict, add_user, NameNotUniqueException, is_username_taken, get_user, \
    UnknownUserException, authenticate_user, AuthenticationException
from games.domainmodel.model import Game, Publisher, Genre, Review, User
from games.home.services import get_recently_added_games, get_action_games
from games.info.services import get_recommended_games, get_game_by_id
from games.profile.services import add_game_to_favourites, remove_game_from_favourites, get_favourite_games, get_reviews
from games.reviews.services import add_new_review
from games.sidebar.services import search_by_title, search_by_genre, search_by_publisher, get_genres_and_urls, \
    get_publishers_and_urls, game_by_genre, game_by_publisher


@pytest.fixture
def test_repo():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)
    return test_repo


# allgames service
def test_get_all_games(test_repo):
    # test that correct number and type of objects are returned
    all_games = get_all_games(test_repo)
    assert len(all_games) == 877
    assert all(isinstance(game, Game) for game in all_games)

    # test that the games are ordered by latest release date
    for i in range(len(all_games) - 1):
        assert datetime.strptime(all_games[i].release_date, "%b %d, %Y") \
               >= datetime.strptime(all_games[i + 1].release_date, "%b %d, %Y")


def test_pagination(test_repo):
    # test that correct number and type of objects are returned
    all_games = get_all_games(test_repo)
    visible_games = pagination(16, 1, all_games)
    assert len(visible_games) == 16
    assert all(isinstance(game, Game) for game in visible_games)

    # test that the correct games are being shown
    assert visible_games == all_games[0:16]
    visible_games = pagination(16, 2, all_games)
    assert visible_games == all_games[16:32]

    # test the last page of games (less than the max number of games per page)
    last_page = int(len(all_games) / 16) + 1
    print(last_page)
    visible_games = pagination(16, last_page, all_games)
    assert len(visible_games) == len(all_games) % 16
    assert visible_games == all_games[(16 * (last_page - 1)):]


# home service
def test_get_recently_added_games(test_repo):
    # test that the correct number and type of objects are returned
    recent_games = get_recently_added_games(test_repo, 4)
    assert len(recent_games) == 4
    assert all(isinstance(game, Game) for game in recent_games)

    # test that the games are ordered by latest release date
    for i in range(len(recent_games) - 1):
        assert datetime.strptime(recent_games[i].release_date, "%b %d, %Y") \
               >= datetime.strptime(recent_games[i + 1].release_date, "%b %d, %Y")


def test_get_action_games(test_repo):
    # test that correct number and type of objects are returned
    action_games = get_action_games(test_repo, 4)
    assert len(action_games) == 4
    assert all(isinstance(game, Game) for game in action_games)

    # test that all games have the genre 'Action'
    assert all(Genre('Action') in game.genres for game in action_games)


# info service
def test_get_game_by_id(test_repo):
    # test a game that exists
    # check if all dictionary values are the same as the game attributes
    game = test_repo.get_game(1995240)
    game_test = get_game_by_id(test_repo, 1995240)
    assert game_test.title == game.title
    assert game_test.price == game.price
    assert game_test.publisher == game.publisher
    assert game_test.genres == game.genres
    assert game_test.release_date == game.release_date
    assert game_test.description == game.description
    assert game_test.image_url == game.image_url
    assert game_test.trailer_url == game.trailer_url
    assert game_test.reviews == game.reviews

    # check if all dictionary values are of the correct type
    assert isinstance(game_test.title, str)
    assert isinstance(game_test.price, int | float)
    assert isinstance(game_test.publisher, Publisher)
    assert isinstance(game_test.genres, list)
    assert all(isinstance(genre, Genre) for genre in game_test.genres)
    assert isinstance(game_test.release_date, str)
    assert isinstance(game_test.description, str)
    assert isinstance(game_test.image_url, str)
    assert 'header.jpg' in game_test.image_url
    assert isinstance(game_test.trailer_url, str)
    assert ('.jpg' in game_test.trailer_url or '.mp4' in game_test.trailer_url)
    assert isinstance(game_test.reviews, list)
    assert all(isinstance(review, Review) for review in game_test.reviews)
    assert isinstance(game_test.recommended_games, list)
    assert all(isinstance(rec, Game) for rec in game_test.recommended_games)

    # test a game that doesn't exist in the repo
    game = Game(127, 'Neo Culture Technology')
    game_dict = get_game_by_id(test_repo, 1)
    assert game_dict is None

    # test invalid input
    game_dict = get_game_by_id(test_repo, '1')
    assert game_dict is None


def test_get_recommended_games(test_repo):
    # test that current game is not in the list of recommended games
    current_game = test_repo.get_game(1995240)
    recs = get_recommended_games(test_repo, current_game.genres, current_game)
    assert current_game not in recs

    # test that each game only occurs once in the list
    counts = Counter(recs)
    assert all(count == 1 for count in counts.values())

    # test that all games have the same number of genres in common with the current game
    common_genres = [len(set(current_game.genres).intersection(game.genres)) for game in recs]
    assert all(num_genres == common_genres[0] for num_genres in common_genres)


# sidebar service
def test_search_by_title(test_repo):
    # test an existing game title
    games = search_by_title(test_repo, "Automobilista 2")
    assert len(games) == 1
    assert all(isinstance(game, Game) for game in games)
    assert games[0] == Game(1066890, "Automobilista 2")

    # test a search string to return multiple games
    games = search_by_title(test_repo, "ball")
    assert len(games) == 15
    assert all(isinstance(game, Game) for game in games)

    # test that the search function is not case-sensitive
    games = search_by_title(test_repo, "BAlL")
    assert len(games) == 15

    # test that leading and trailing spaces are removed
    games = search_by_title(test_repo, "   Ball   ")
    assert len(games) == 15

    # test a search string that will not return any game
    games = search_by_title(test_repo, "abcdefghijklmnopqrstuvwxyz")
    assert len(games) == 0

    # test that an empty string returns an empty list
    games = search_by_title(test_repo, "")
    assert len(games) == 0

    # test that a string of only space bars returns an empty list
    games = search_by_title(test_repo, "   ")
    assert len(games) == 0


def test_search_by_genre(test_repo):
    # test an existing genre
    games = search_by_genre(test_repo, "Action")
    assert len(games) == 380
    assert all(isinstance(game, Game) for game in games)

    # test a search string that can involve multiple genres
    games = search_by_genre(test_repo, "ac")
    assert len(games) == 430
    assert all(isinstance(game, Game) for game in games)

    # test that the search function is not case-sensitive
    games = search_by_genre(test_repo, "AC")
    assert len(games) == 430

    # test that leading and trailing spaces are removed
    games = search_by_genre(test_repo, "   Ac   ")
    assert len(games) == 430

    # test a search string that will not return any game
    games = search_by_genre(test_repo, "abcdefghijklmnopqrstuvwxyz")
    assert len(games) == 0

    # test that an empty string returns an empty list
    games = search_by_genre(test_repo, "")
    assert len(games) == 0

    # test that a string of only space bars returns an empty list
    games = search_by_genre(test_repo, "   ")
    assert len(games) == 0


def test_search_by_publisher(test_repo):
    # test an existing publisher
    games = search_by_publisher(test_repo, "Activision")
    assert len(games) == 1
    assert all(isinstance(game, Game) for game in games)

    # test a search string that can involve multiple publishers
    games = search_by_publisher(test_repo, "ac")
    assert len(games) == 60
    assert all(isinstance(game, Game) for game in games)

    # test that the search function is not case-sensitive
    games = search_by_publisher(test_repo, "AC")
    assert len(games) == 60

    # test that leading and trailing spaces are removed
    games = search_by_publisher(test_repo, "   Ac   ")
    assert len(games) == 60

    # test a search string that will not return any game
    games = search_by_publisher(test_repo, "abcdefghijklmnopqrstuvwxyz")
    assert len(games) == 0

    # test that an empty string returns an empty list
    games = search_by_publisher(test_repo, "")
    assert len(games) == 0

    # test that a string of only space bars returns an empty list
    games = search_by_publisher(test_repo, "   ")
    assert len(games) == 0


def test_get_genres_and_urls(test_repo):
    # test that correct number of urls are returned
    genre_urls = get_genres_and_urls(test_repo)
    assert len(genre_urls) == 24

    # test that the correct url is returned, accounting for spaces and symbols
    assert genre_urls["Action"] == "http://127.0.0.1:5000/games_by_genre?genre=Action"
    assert genre_urls["Animation & Modeling"] == \
           "http://127.0.0.1:5000/games_by_genre?genre=Animation%20%26%20Modeling"


def test_get_publishers_and_urls(test_repo):
    # test that correct number of urls are returned
    publisher_urls = get_publishers_and_urls(test_repo)
    assert len(publisher_urls) == 798

    # test that the correct url is returned, accounting for spaces and symbols
    assert publisher_urls["Activision"] == "http://127.0.0.1:5000/games_by_publisher?publisher=Activision"
    assert publisher_urls["13-lab,azimuth team"] == \
           "http://127.0.0.1:5000/games_by_publisher?publisher=13-lab%2Cazimuth%20team"


def test_game_by_genre(test_repo):
    # test that the correct number of games are returned for a given genre
    # test that all objects returned are of Game type
    games = game_by_genre(test_repo, "Action")
    assert len(games) == 380
    assert all(isinstance(game, Game) for game in games)


def test_game_by_publisher(test_repo):
    # test that the correct number of games are returned for a given publisher
    # test that all objects returned are of Game type
    games = game_by_publisher(test_repo, "Activision")
    assert len(games) == 1
    assert all(isinstance(game, Game) for game in games)


# authentication service
def test_add_user(test_repo):
    # test that a new user can be added to the repo

    # uuid generates a unique string each time
    # so that subsequent runs of pytest won't cause error
    # as each new user gets written to the .csv file
    new_user = (str(uuid.uuid4()))[0:10]
    add_user(new_user, "Passw0rd", test_repo)
    user = test_repo.get_user(new_user)
    assert user.username == new_user

    # test that an existing user raises an exception
    with pytest.raises(NameNotUniqueException):
        add_user("oliviarodrigo", "Passw0rd", test_repo)


def test_get_user(test_repo):
    # test that an existing user can be obtained
    user = get_user("oliviarodrigo", test_repo)
    assert user['user_name'] == "oliviarodrigo"

    # test that an invalid user raises an exception
    with pytest.raises(UnknownUserException):
        get_user("arianagrande", test_repo)


def test_authenticate_user(test_repo):
    # test an existing user with correct password doesn't raise an exception
    authenticate_user('oliviarodrigo', 'Passw0rd', test_repo)

    # test an existing user with incorrect password
    with pytest.raises(AuthenticationException):
        authenticate_user('oliviarodrigo', 'Password', test_repo)

    # test an invalid user
    with pytest.raises(AuthenticationException):
        authenticate_user('arianagrande', 'Passw0rd', test_repo)


def test_is_username_taken(test_repo):
    assert is_username_taken("oliviarodrigo", test_repo) is True
    assert is_username_taken("arianagrande", test_repo) is False


def test_user_to_dict():
    test_user = User("oliviarodrigo", "Passw0rd")
    user_dict = user_to_dict(test_user)
    assert user_dict == {'user_name': 'oliviarodrigo', 'password': 'Passw0rd'}


# review service
def test_add_new_review(test_repo):
    # create a new review and test that it is added to the user's reviews
    user = test_repo.get_user("baekhyunbyun")
    game = test_repo.get_game(316260)
    rating = random.randint(1, 5)
    comment = (str(uuid.uuid4()))[0:100]
    current_datetime = str(datetime.now())

    add_new_review(test_repo, user.username, game.game_id, rating, comment, current_datetime)
    review = Review(user, game, rating, comment, current_datetime)
    assert review in user.reviews


# profile service
def test_get_favourite_games(test_repo):
    # test that the correct games are returned
    # test that they are all the correct object type
    user = test_repo.get_user("oliviarodrigo")
    game1 = test_repo.get_game(316260)
    game2 = test_repo.get_game(1995240)
    user.add_favourite_game(game1)
    user.add_favourite_game(game2)

    games = get_favourite_games(user.username, test_repo)
    assert len(games) == 2
    assert game1 in games
    assert game2 in games
    assert all(isinstance(game, Game) for game in games)


def test_get_reviews(test_repo):
    # test that the correct reviews are returned
    # test that they are all the correct object type
    user = test_repo.get_user("marklee")
    reviews = get_reviews(user.username, test_repo)
    assert len(reviews) == 6
    assert all(isinstance(review, Review) for review in reviews)


def test_add_game_to_favourites(test_repo):
    user = test_repo.get_user("oliviarodrigo")
    game = test_repo.get_game(316260)

    # test successful addition of game
    add_game_to_favourites(user.username, game.game_id, test_repo)
    assert game in user.favourite_games

    # test invalid user or invalid game
    with pytest.raises(ValueError):
        add_game_to_favourites("arianagrande", 316260, test_repo)
    with pytest.raises(ValueError):
        add_game_to_favourites("oliviarodrigo", 316259, test_repo)


def test_remove_game_from_favourites(test_repo):
    user = test_repo.get_user("oliviarodrigo")
    game = test_repo.get_game(316260)

    # test successful removal of game
    add_game_to_favourites(user.username, game.game_id, test_repo)
    remove_game_from_favourites(user.username, game.game_id, test_repo)
    assert game not in user.favourite_games

    # test invalid user or invalid game
    with pytest.raises(ValueError):
        add_game_to_favourites("arianagrande", 316260, test_repo)
    with pytest.raises(ValueError):
        add_game_to_favourites("oliviarodrigo", 316259, test_repo)
