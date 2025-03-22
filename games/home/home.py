from flask import Blueprint, render_template, session
import games.adapters.repository as repo
import games.home.services as services
import games.sidebar.services as sidebar_services

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    recently_added_games = services.get_recently_added_games(repo.repo_instance, 4)
    action_games = services.get_action_games(repo.repo_instance, 4)

    genre_urls = sidebar_services.get_genres_and_urls(repo.repo_instance)
    publisher_urls = sidebar_services.get_publishers_and_urls(repo.repo_instance)

    user = session.get('user_name')

    return render_template('home.html', genre_urls=genre_urls, publisher_urls=publisher_urls,
                           recently_added_games=recently_added_games, action_games=action_games, user=user)
