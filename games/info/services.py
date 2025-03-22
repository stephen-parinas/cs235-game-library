from collections import Counter
from typing import List

from games.domainmodel.model import Game, Genre
from games.adapters.repository import AbstractRepository


def get_game_by_id(repo: AbstractRepository, game_id: int):
    game = repo.get_game(game_id)
    if game:
        if len(game.recommended_games) == 0:
            recommended_games = get_recommended_games(repo, game.genres, game)
            recommended_games = repo.sort_games_by_date(recommended_games)
            for g in recommended_games:
                game.add_recommended_game(g)
            repo.update_game(game)
        return game
    else:
        return None


def get_recommended_games(repo: AbstractRepository, game_genres: List[Genre], current_game: Game):
    # find all games with genres in common
    games = list()
    for genre in game_genres:
        games.extend(repo.get_game_by_genre(genre))

    # remove all instances of current game from the list
    games = [game for game in games if game != current_game]

    # determine the games with the most genres in common with the current game
    genre_counts = Counter(games)
    max_genre_count = max(genre_counts.values())
    recommended_games = [game for game, count in genre_counts.items() if count == max_genre_count]

    # remove any duplications from the list
    recommended_games = list(set(recommended_games))
    return recommended_games
