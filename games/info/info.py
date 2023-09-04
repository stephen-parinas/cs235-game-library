from flask import Blueprint, render_template

from games.info import services
import games.adapters.repository as repo
import games.sidebar.services as sidebar_services

# Configure blueprint
info_blueprint = Blueprint('info_bp', __name__)


@info_blueprint.route('/info/<int:game_id>', methods=['GET'])
def get_game_info(game_id):
    game = services.get_game_by_id(repo.repo_instance, game_id)

    genre_urls = sidebar_services.get_genres_and_urls(repo.repo_instance)
    publisher_urls = sidebar_services.get_publishers_and_urls(repo.repo_instance)

    return render_template('gameInfo.html', game=game, genre_urls=genre_urls, publisher_urls=publisher_urls)



