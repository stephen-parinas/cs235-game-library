from flask import Blueprint, render_template, request, session
from games.sidebar import services

import games.adapters.repository as repo
import games.allgames.services as allgames_services

# Configure blueprint
sidebar_blueprint = Blueprint('sidebar_bp', __name__)


@sidebar_blueprint.route('/search/<int:page>', methods=['GET'])
@sidebar_blueprint.route('/search/', defaults={'page': 1}, methods=['GET'])
def search(page, search_query="", filter_criteria="title"):
    search_results = list()

    if request.method == 'GET':
        search_query = request.args.get('query', default='', type=str)
        filter_criteria = request.args.get('filter')
        if filter_criteria == 'title':
            search_results = services.search_by_title(repo.repo_instance, search_query)
        elif filter_criteria == 'genre':
            search_results = services.search_by_genre(repo.repo_instance, search_query)
        elif filter_criteria == 'publisher':
            search_results = services.search_by_publisher(repo.repo_instance, search_query)
        else:
            search_results = []

    total_games = len(search_results)
    visible_games = allgames_services.pagination(16, page, search_results)

    genre_urls = services.get_genres_and_urls(repo.repo_instance)
    publisher_urls = services.get_publishers_and_urls(repo.repo_instance)

    user = session.get('user_name')

    return render_template('allGames.html', title=f"Search results for: {search_query}",
                           search_query=search_query, filter_criteria=filter_criteria,
                           list_of_games=visible_games, page=page, total_games=total_games,
                           genre_urls=genre_urls, publisher_urls=publisher_urls, user=user)


@sidebar_blueprint.route('/games_by_genre/<int:page>')
@sidebar_blueprint.route('/games_by_genre', defaults={'page': 1})
def games_by_genre(page):
    genre = request.args.get('genre')
    games = services.game_by_genre(repo.repo_instance, genre)

    total_games = len(games)
    visible_games = allgames_services.pagination(16, page, games)

    genre_urls = services.get_genres_and_urls(repo.repo_instance)
    publisher_urls = services.get_publishers_and_urls(repo.repo_instance)

    user = session.get('user_name')

    return render_template('allGames.html', title=genre, genre=genre, list_of_games=visible_games, page=page,
                           total_games=total_games, genre_urls=genre_urls, publisher_urls=publisher_urls, user=user)


@sidebar_blueprint.route('/games_by_publisher/<int:page>')
@sidebar_blueprint.route('/games_by_publisher', defaults={'page': 1})
def games_by_publisher(page):
    publisher = request.args.get('publisher')
    games = services.game_by_publisher(repo.repo_instance, publisher)

    total_games = len(games)
    visible_games = allgames_services.pagination(16, page, games)

    genre_urls = services.get_genres_and_urls(repo.repo_instance)
    publisher_urls = services.get_publishers_and_urls(repo.repo_instance)

    user = session.get('user_name')

    return render_template('allGames.html', title=publisher, publisher=publisher, list_of_games=visible_games, page=page,
                           total_games=total_games, genre_urls=genre_urls, publisher_urls=publisher_urls, user=user)

