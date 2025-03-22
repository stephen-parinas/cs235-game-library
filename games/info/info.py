from flask import Blueprint, render_template, session

from games.info import services
import games.adapters.repository as repo
import games.profile.services as profile_services
import games.sidebar.services as sidebar_services
from games.reviews.reviews import ReviewForm

# Configure blueprint
info_blueprint = Blueprint('info_bp', __name__)


@info_blueprint.route('/info/<int:game_id>', methods=['GET'])
def get_game_info(game_id):
    game = services.get_game_by_id(repo.repo_instance, game_id)

    genre_urls = sidebar_services.get_genres_and_urls(repo.repo_instance)
    publisher_urls = sidebar_services.get_publishers_and_urls(repo.repo_instance)

    user = session.get('user_name')
    favourite_games = []
    form = ReviewForm()

    if user:
        favourite_games = profile_services.get_favourite_games(user, repo.repo_instance)
        form.username.data = user
        form.game_id.data = game_id

    return render_template('gameInfo/gameInfo.html', game=game, genre_urls=genre_urls, publisher_urls=publisher_urls,
                           favourite_games=favourite_games, user=user, form=form)



