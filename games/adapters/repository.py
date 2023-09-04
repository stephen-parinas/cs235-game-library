import abc

from games.domainmodel.model import Game, Genre, Publisher, Review

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_game(self, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, publisher: Publisher):
        raise NotImplementedError

    @abc.abstractmethod
    def get_game(self, target_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_by_genre(self, target_genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_by_publisher(self, target_publisher: Publisher):
        raise NotImplementedError

    @abc.abstractmethod
    def sort_games_by_date(self, games: list):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_games(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_genres(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_publishers(self):
        raise NotImplementedError

    @abc.abstractmethod
    def search_games_by_title(self, search_query: str):
        raise NotImplementedError

    @abc.abstractmethod
    def search_games_by_genre(self, search_query: str):
        raise NotImplementedError

    @abc.abstractmethod
    def search_games_by_publisher(self, search_query: str):
        raise NotImplementedError
