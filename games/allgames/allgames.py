from flask import Blueprint, render_template, session

import games.adapters.repository as repo
import games.allgames.services as services
import games.sidebar.services as sidebar_services

# Configure blueprint
allgames_blueprint = Blueprint('allgames_bp', __name__)


@allgames_blueprint.route('/all_games/<int:page>')
@allgames_blueprint.route('/all_games', defaults={'page': 1})
def show_all_games(page):
    list_of_all_games = services.get_all_games(repo.repo_instance)

    total_games = len(list_of_all_games)
    visible_games = services.pagination(16, page, list_of_all_games)

    genre_urls = sidebar_services.get_genres_and_urls(repo.repo_instance)
    publisher_urls = sidebar_services.get_publishers_and_urls(repo.repo_instance)

    user = session.get('user_name')
    
    return render_template('allGames.html', title="Browse All Games", list_of_games=visible_games,page=page,
                           total_games=total_games, genre_urls=genre_urls, publisher_urls=publisher_urls, user=user)
