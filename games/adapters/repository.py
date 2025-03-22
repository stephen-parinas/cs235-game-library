import abc

from games.domainmodel.model import Game, Genre, Publisher, Review, User

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

    @abc.abstractmethod
    def add_review(self, review: Review):
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.game is None or review not in review.game.reviews:
            raise RepositoryException('Review not correctly attached to an Game')

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_users(self):
        raise NotImplementedError

    @abc.abstractmethod
    def update_game(self, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def update_user(self, user: User):
        raise NotImplementedError
