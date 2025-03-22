from pathlib import Path
from bisect import insort_left
from datetime import datetime

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, Publisher, Review, User


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__games = list()
        self.__genres = list()
        self.__publishers = list()
        self.__users = list()

    def add_game(self, game: Game):
        if isinstance(game, Game) and game not in self.__games:
            insort_left(self.__games, game)

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre) and genre not in self.__genres:
            insort_left(self.__genres, genre)

    def add_publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher) and publisher not in self.__publishers:
            insort_left(self.__publishers, publisher)

    def get_game(self, target_id: int) -> Game | None:
        for game in self.__games:
            if game.game_id == target_id:
                return game
        return None

    def get_game_by_genre(self, target_genre: Genre) -> list:
        return [game for game in self.__games if target_genre in game.genres]

    def get_game_by_publisher(self, target_publisher: Publisher) -> list:
        return [game for game in self.__games if target_publisher == game.publisher]

    def sort_games_by_date(self, games: list):
        sorted_games_date = sorted(games, key=lambda r: datetime.strptime(r.release_date, "%b %d, %Y"),
                                   reverse=True)
        return sorted_games_date

    def get_all_games(self) -> list:
        return self.__games

    def get_all_genres(self) -> list:
        return self.__genres

    def get_all_publishers(self) -> list:
        return self.__publishers

    def search_games_by_title(self, search_query: str) -> list:
        return [game for game in self.__games if search_query.lower() in game.title.lower()]

    def search_games_by_genre(self, search_query: str) -> list:
        genres = [genre for genre in self.__genres if search_query.lower() in genre.genre_name.lower()]
        # prevent games from being duplicated when added to list
        games_set = set()
        for genre in genres:
            games_set.update(self.get_game_by_genre(genre))
        return list(games_set)

    def search_games_by_publisher(self, search_query: str) -> list:
        pubs = [pub for pub in self.__publishers if search_query.lower() in pub.publisher_name.lower()]
        # prevent games from being duplicated when added to list
        games_set = set()
        for pub in pubs:
            games_set.update(self.get_game_by_publisher(pub))
        return list(games_set)

    def add_review(self, review: Review):
        if isinstance(review, Review):
            if review in review.user.reviews:
                return
            if review in review.game.reviews:
                return
            review.user.add_review(review)
            review.game.add_review(review)
            # data_path = Path('games') / 'adapters' / 'data'
            # write_review(data_path, review)

    def add_user(self, user: User):
        if isinstance(user, User) and user not in self.__users:
            insort_left(self.__users, user)
            # data_path = Path('games') / 'adapters' / 'data'
            # write_user(data_path, user)

    def get_user(self, username: str) -> User | None:
        for user in self.__users:
            if user.username.lower() == username.lower():
                return user
        return None

    def get_all_users(self) -> list:
        return self.__users

    def update_game(self, game: Game):
        super()

    def update_user(self, user: User):
        super()
