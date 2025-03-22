from pathlib import Path
import os
from games.adapters.repository import AbstractRepository
from games.adapters.csv_data_importer import GameFileCSVReader


def populate(data_path: Path, repo: AbstractRepository, database_mode=False):
    games_file_name = str(Path(data_path) / "games.csv")
    games_file_name = os.path.join(data_path, "games.csv")
    users_file_name = str(Path(data_path) / "users.csv")
    reader = GameFileCSVReader(games_file_name,users_file_name)
    reader.read_game_csv_file()
    games = reader.dataset_of_games
    genres = reader.dataset_of_genres

    for game in games:
        repo.add_game(game)

    for genre in genres:
        repo.add_genre(genre)

    for publisher in reader.dataset_of_publishers:
        repo.add_publisher(publisher)

    if database_mode is False:
        reader.read_user_csv_file()

        for user in reader.dataset_of_users:
            repo.add_user(user)

            for review in user.reviews:
                game = repo.get_game(review.game.game_id)
                game.add_review(review)
