"""Initialize Flask app."""

from flask import Flask
from pathlib import Path
import games.adapters.repository as repo
from games.adapters.memory_repository import MemoryRepository, populate


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)


    #app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    repo.repo_instance = MemoryRepository()
    # fill the content of the repository from the provided csv files
    populate(data_path, repo.repo_instance)

    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .info import info
        app.register_blueprint(info.info_blueprint)

        from .allgames import allgames
        app.register_blueprint(allgames.allgames_blueprint)

        from .sidebar import sidebar
        app.register_blueprint(sidebar.sidebar_blueprint)

        return app