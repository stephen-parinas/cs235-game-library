from urllib.parse import quote

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Genre, Publisher


def search_by_title(repo: AbstractRepository, search_query: str):
    search_query = search_query.strip()
    if search_query == "":
        return []
    else:
        return repo.sort_games_by_date(repo.search_games_by_title(search_query))


def search_by_genre(repo: AbstractRepository, search_query: str):
    search_query = search_query.strip()
    if search_query == "":
        return []
    else:
        return repo.sort_games_by_date(repo.search_games_by_genre(search_query))


def search_by_publisher(repo: AbstractRepository, search_query: str):
    search_query = search_query.strip()
    if search_query == "":
        return []
    else:
        return repo.sort_games_by_date(repo.search_games_by_publisher(search_query))


def get_genres_and_urls(repo: AbstractRepository):
    genres = repo.get_all_genres()
    genre_names = [genre.genre_name for genre in genres]
    genre_urls = dict()
    for genre_name in genre_names:
        genre_urls[genre_name] = f"http://127.0.0.1:5000/games_by_genre?genre={quote(genre_name)}"
    return genre_urls


def get_publishers_and_urls(repo: AbstractRepository):
    publishers = repo.get_all_publishers()
    publisher_names = [publisher.publisher_name for publisher in publishers]
    publisher_urls = dict()
    for publisher_name in publisher_names:
        publisher_urls[publisher_name] = f"http://127.0.0.1:5000/games_by_publisher?publisher={quote(publisher_name)}"
    return publisher_urls


def game_by_genre(repo: AbstractRepository, target_genre: str):
    return repo.get_game_by_genre(Genre(target_genre))


def game_by_publisher(repo: AbstractRepository, target_publisher: str):
    return repo.get_game_by_publisher(Publisher(target_publisher))
