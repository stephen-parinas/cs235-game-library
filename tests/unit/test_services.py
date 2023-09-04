from collections import Counter
from datetime import datetime
from pathlib import Path

import pytest
from games.adapters.memory_repository import MemoryRepository, populate
from games.allgames.services import get_all_games, pagination
from games.domainmodel.model import Game, Publisher, Genre, Review
from games.home.services import get_recently_added_games, get_action_games
from games.info.services import get_recommended_games, get_game_by_id
from games.sidebar.services import search_by_title, search_by_genre, search_by_publisher, get_genres_and_urls, \
    get_publishers_and_urls, game_by_genre, game_by_publisher


# allgames service
def test_get_all_games():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

    # test that correct number and type of objects are returned
    all_games = get_all_games(test_repo)
    assert len(all_games) == 877
    assert all(isinstance(game, Game) for game in all_games)

    # test that the games are ordered by latest release date
    for i in range(len(all_games) - 1):
        assert datetime.strptime(all_games[i].release_date, "%b %d, %Y") \
               >= datetime.strptime(all_games[i + 1].release_date, "%b %d, %Y")


def test_pagination():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

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
def test_get_recently_added_games():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

    # test that the correct number and type of objects are returned
    recent_games = get_recently_added_games(test_repo, 4)
    assert len(recent_games) == 4
    assert all(isinstance(game, Game) for game in recent_games)

    # test that the games are ordered by latest release date
    for i in range(len(recent_games) - 1):
        assert datetime.strptime(recent_games[i].release_date, "%b %d, %Y") \
               >= datetime.strptime(recent_games[i + 1].release_date, "%b %d, %Y")


def test_get_action_games():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

    # test that correct number and type of objects are returned
    action_games = get_action_games(test_repo, 4)
    assert len(action_games) == 4
    assert all(isinstance(game, Game) for game in action_games)

    # test that all games have the genre 'Action'
    assert all(Genre('Action') in game.genres for game in action_games)


# info service
def test_get_game_by_id():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

    # test a game that exists
    # check if all dictionary values are the same as the game attributes
    game = test_repo.get_game(1995240)
    game_dict = get_game_by_id(test_repo, 1995240)
    assert game_dict['title'] == game.title
    assert game_dict['price'] == game.price
    assert game_dict['publisher'] == game.publisher
    assert game_dict['genres'] == game.genres
    assert game_dict['release_date'] == game.release_date
    assert game_dict['description'] == game.description
    assert game_dict['image_url'] == game.image_url
    assert game_dict['trailer'] == game.trailer_url
    assert game_dict['reviews'] == game.reviews
    assert game_dict['recommended_games'] == get_recommended_games(test_repo, game.genres, game)

    # check if all dictionary values are of the correct type
    assert isinstance(game_dict['title'], str)
    assert isinstance(game_dict['price'], int | float)
    assert isinstance(game_dict['publisher'], Publisher)
    assert isinstance(game_dict['genres'], list)
    assert all(isinstance(genre, Genre) for genre in game_dict['genres'])
    assert isinstance(game_dict['release_date'], str)
    assert isinstance(game_dict['description'], str)
    assert isinstance(game_dict['image_url'], str)
    assert 'header.jpg' in game_dict['image_url']
    assert isinstance(game_dict['trailer'], str)
    assert ('.jpg' in game_dict['image_url'] or '.mp4' in game_dict['image_url'])
    assert isinstance(game_dict['reviews'], list)
    assert all(isinstance(review, Review) for review in game_dict['reviews'])
    assert isinstance(game_dict['recommended_games'], list)
    assert all(isinstance(rec, Game) for rec in game_dict['recommended_games'])

    # test a game that doesn't exist in the repo
    game = Game(127, 'Neo Culture Technology')
    game_dict = get_game_by_id(test_repo, 1)
    assert game_dict is None

    # test invalid input
    game_dict = get_game_by_id(test_repo, '1')
    assert game_dict is None


def test_get_recommended_games():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

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
def test_search_by_title():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

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


def test_search_by_genre():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

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


def test_search_by_publisher():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

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


def test_get_genres_and_urls():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

    # test that correct number of urls are returned
    genre_urls = get_genres_and_urls(test_repo)
    assert len(genre_urls) == 24

    # test that the correct url is returned, accounting for spaces and symbols
    assert genre_urls["Action"] == "http://127.0.0.1:5000/games_by_genre?genre=Action"
    assert genre_urls["Animation & Modeling"] == \
           "http://127.0.0.1:5000/games_by_genre?genre=Animation%20%26%20Modeling"


def test_get_publishers_and_urls():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

    # test that correct number of urls are returned
    publisher_urls = get_publishers_and_urls(test_repo)
    assert len(publisher_urls) == 798

    # test that the correct url is returned, accounting for spaces and symbols
    assert publisher_urls["Activision"] == "http://127.0.0.1:5000/games_by_publisher?publisher=Activision"
    assert publisher_urls["13-lab,azimuth team"] == \
           "http://127.0.0.1:5000/games_by_publisher?publisher=13-lab%2Cazimuth%20team"


def test_game_by_genre():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

    # test that the correct number of games are returned for a given genre
    # test that all objects returned are of Game type
    games = game_by_genre(test_repo, "Action")
    assert len(games) == 380
    assert all(isinstance(game, Game) for game in games)


def test_game_by_publisher():
    test_repo = MemoryRepository()
    test_path = Path.cwd() / 'games' / 'adapters' / 'data'
    populate(test_path, test_repo)

    # test that the correct number of games are returned for a given publisher
    # test that all objects returned are of Game type
    games = game_by_publisher(test_repo, "Activision")
    assert len(games) == 1
    assert all(isinstance(game, Game) for game in games)
