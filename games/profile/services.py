from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User


def get_favourite_games(username, repo: AbstractRepository):
    user: User = repo.get_user(username)
    return user.favourite_games


def get_reviews(username, repo: AbstractRepository):
    user: User = repo.get_user(username)
    return user.reviews


def add_game_to_favourites(username, game_id, repo: AbstractRepository):
    user: User = repo.get_user(username)
    game = repo.get_game(game_id)
    if user is None or game is None:
        raise ValueError("User or Game not found")
    else:
        user.add_favourite_game(game)
        repo.update_user(user)


def remove_game_from_favourites(username, game_id, repo: AbstractRepository):
    user: User = repo.get_user(username)
    game = repo.get_game(game_id)
    if user is None or game is None:
        raise ValueError("User or Game not found")
    else:
        user.remove_favourite_game(game)
        repo.update_game(game)
