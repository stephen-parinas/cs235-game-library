from datetime import datetime

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Review, User


def add_new_review(repo: AbstractRepository, username: str, game_id: int, rating: int, comment: str, current_datetime: str):
    # Create new review object
    user = repo.get_user(username)
    game = repo.get_game(game_id)
    review = Review(user, game, rating, comment, current_datetime)

    # Add review to both user and game objects, and write to the CSV file
    repo.add_review(review)
    repo.update_user(user)

    game.update_average_rating()
    repo.update_game(game)
