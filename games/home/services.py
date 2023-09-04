from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Genre


def get_recently_added_games(repo: AbstractRepository, quantity: int):
    games = repo.sort_games_by_date(repo.get_all_games())
    recently_added = games[:quantity]
    return recently_added


def get_action_games(repo: AbstractRepository, quantity: int):
    action_games = repo.get_game_by_genre(Genre("Action"))[:quantity]
    return action_games
