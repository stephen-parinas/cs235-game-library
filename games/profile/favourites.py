from flask import Blueprint, request, redirect, url_for, session

from games.authentication.authentication import login_required

import games.adapters.repository as repo
import games.profile.services as services

favourites_blueprint= Blueprint('favourites_bp', __name__)


@favourites_blueprint.route('/add_to_favourites/<int:game_id>', methods=['GET', 'POST'])
@login_required
def add_to_favourites(game_id):
    username = session.get('user_name')
    services.add_game_to_favourites(username, game_id, repo.repo_instance)
    return redirect(url_for('info_bp.get_game_info', game_id=game_id))


@favourites_blueprint.route('/remove_from_favourites/<int:game_id>', methods=['GET', 'POST'])
@login_required
def remove_from_favourites(game_id):
    username = session.get('user_name')
    services.remove_game_from_favourites(username, game_id, repo.repo_instance)
    return redirect(url_for('info_bp.get_game_info', game_id=game_id))
