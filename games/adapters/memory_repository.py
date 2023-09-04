from pathlib import Path
from bisect import insort_left
from datetime import datetime

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, Publisher
from games.adapters.datareader.csvdatareader import GameFileCSVReader


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__games = list()
        self.__genres = list()
        self.__publishers = list()

    def add_game(self, game: Game):
        if isinstance(game, Game) and game not in self.__games:
            insort_left(self.__games, game)

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre) and genre not in self.__genres:
            insort_left(self.__genres, genre)

    def add_publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher) and publisher not in self.__publishers:
            insort_left(self.__publishers, publisher)

    def get_game(self, target_id: int):
        for game in self.__games:
            if game.game_id == target_id:
                return game
        return None

    def get_game_by_genre(self, target_genre: Genre):
        return [game for game in self.__games if target_genre in game.genres]

    def get_game_by_publisher(self, target_publisher: Publisher):
        return [game for game in self.__games if target_publisher == game.publisher]

    def sort_games_by_date(self, games: list):
        sorted_games_date = sorted(games, key=lambda r: datetime.strptime(r.release_date, "%b %d, %Y"),
                                   reverse=True)
        return sorted_games_date

    def get_all_games(self):
        return self.__games

    def get_all_genres(self):
        return self.__genres

    def get_all_publishers(self):
        return self.__publishers

    def search_games_by_title(self, search_query: str):
        return [game for game in self.__games if search_query.lower() in game.title.lower()]

    def search_games_by_genre(self, search_query: str):
        genres = [genre for genre in self.__genres if search_query.lower() in genre.genre_name.lower()]
        # prevent games from being duplicated when added to list
        games_set = set()
        for genre in genres:
            games_set.update(self.get_game_by_genre(genre))
        return list(games_set)

    def search_games_by_publisher(self, search_query: str):
        pubs = [pub for pub in self.__publishers if search_query.lower() in pub.publisher_name.lower()]
        # prevent games from being duplicated when added to list
        games_set = set()
        for pub in pubs:
            games_set.update(self.get_game_by_publisher(pub))
        return list(games_set)


def populate(data_path: Path, repo: MemoryRepository):
    games_file_name = str(Path(data_path) / "games.csv")
    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()

    for game in reader.dataset_of_games:
        repo.add_game(game)

    for genre in reader.dataset_of_genres:
        repo.add_genre(genre)

    for publisher in reader.dataset_of_publishers:
        repo.add_publisher(publisher)
