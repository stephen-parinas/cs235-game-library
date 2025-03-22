from flask import Blueprint, render_template, session

import games.adapters.repository as repo
import games.profile.services as services
import games.sidebar.services as sidebar_services
from games.authentication.authentication import login_required


user_profile_blueprint = Blueprint('user_profile_bp', __name__)

@user_profile_blueprint.route('/profile',methods=['GET'])
@login_required
def show_profile():
    username = session.get('user_name')
    favourite_games = services.get_favourite_games(username, repo.repo_instance)
    user_reviews = services.get_reviews(username, repo.repo_instance)
    
    genre_urls = sidebar_services.get_genres_and_urls(repo.repo_instance)
    publisher_urls = sidebar_services.get_publishers_and_urls(repo.repo_instance)

    return render_template('profile.html', username=username, favourite_games=favourite_games,user_reviews=user_reviews,genre_urls=genre_urls,publisher_urls=publisher_urls)