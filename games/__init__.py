"""Initialize Flask app."""

from flask import Flask, session
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import games.adapters.repository as repo
import games.adapters.memory_repository as memory_repo
import games.adapters.database_repository as database
from games.adapters import repository_populate
from games.adapters.orm import map_model_to_tables, metadata


def create_app(test_config=None):
    """Construct the core application."""

    app = Flask(__name__)

    app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        repo.repo_instance = memory_repo.MemoryRepository()
        repository_populate.populate(data_path, repo.repo_instance, False)

    elif app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = database.SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")
            connection = database_engine.connect()
            
            clear_mappers()
            metadata.create_all(database_engine)
            
            for table in reversed(metadata.sorted_tables):  
                connection.execute(table.delete())
        
            map_model_to_tables()
            repository_populate.populate(data_path, repo.repo_instance, True)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            map_model_to_tables()

    first_request = True

    @app.before_request
    def clear_user_name_session():
        nonlocal first_request
        if first_request:
            session.pop('user_name', None)
            first_request = False

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

        from .reviews import reviews
        app.register_blueprint(reviews.reviews_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .profile import user_profile
        app.register_blueprint(user_profile.user_profile_blueprint)

        from .profile import favourites
        app.register_blueprint(favourites.favourites_blueprint)

        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database.SqlAlchemyRepository):
                repo.repo_instance.reset_session()
        
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database.SqlAlchemyRepository):
                repo.repo_instance.close_session()

    return app
