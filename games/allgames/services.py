from games.adapters.repository import AbstractRepository


def get_all_games(repo: AbstractRepository):
    return repo.sort_games_by_date(repo.get_all_games())


def pagination(games_per_page: int, page, games_list):
    total_games = len(games_list)

    start_index = (page - 1) * games_per_page
    end_index = start_index + games_per_page

    if end_index > total_games:
        end_index = total_games

    visible_games = games_list[start_index:end_index]

    return visible_games
