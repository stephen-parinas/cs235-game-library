from datetime import datetime
from typing import List

from sqlalchemy import collate
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import scoped_session

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, Publisher, User, Review


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if self.__session is not None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_game(self, game: Game):
        if isinstance(game, Game) and game not in self.get_all_games():
            with self._session_cm as scm:
                scm.session.merge(game)
                scm.commit()

    def add_publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher) and publisher not in self.get_all_publishers():
            with self._session_cm as scm:
                scm.session.merge(publisher)
                scm.commit()

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre) and genre not in self.get_all_genres():
            with self._session_cm as scm:
                scm.session.merge(genre)
                scm.commit()

    def add_user(self, user: User):
        if isinstance(user, User) and user not in self.get_all_users():
            with self._session_cm as scm:
                scm.session.merge(user)
                scm.commit()

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.merge(review)
            scm.commit()

    def get_game(self, target_id: int) -> Game | None:
        game = None
        if isinstance(target_id, int):
            try:
                game = self._session_cm.session.query(Game).filter(Game._Game__game_id == target_id).one()
            except NoResultFound:
                print(f'Game {target_id} was not found')
        return game

    def get_game_by_genre(self, target_genre: Genre) -> list:
        if isinstance(target_genre, Genre):
            games = self._session_cm.session.query(Game).filter(
                Game._Game__genres.any(Genre._Genre__genre_name == target_genre.genre_name)).all()
            return games
        return []

    def get_game_by_publisher(self, target_publisher: Publisher) -> list:
        if isinstance(target_publisher, Publisher):
            games = self._session_cm.session.query(Game).filter(
                Game._Game__publisher.has(Publisher._Publisher__publisher_name == target_publisher.publisher_name)).all()
            return games
        return []

    def get_user(self, username: str) -> User | None:
        user = None
        if isinstance(username, str):
            try:
                user = self._session_cm.session.query(User).filter(User._User__username == username).one()
            except NoResultFound:
                pass
        return user

    def sort_games_by_date(self, games: list):
        sorted_games_date = sorted(games, key=lambda r: datetime.strptime(r.release_date, "%b %d, %Y"),
                                   reverse=True)
        return sorted_games_date

    def get_all_games(self) -> list:
        games = self._session_cm.session.query(Game).all()
        return games

    def get_all_genres(self) -> list:
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def get_all_publishers(self) -> list:
        publishers = self._session_cm.session.query(Publisher).all()
        return publishers

    def get_all_users(self) -> list:
        users = self._session_cm.session.query(User).all()
        return users

    def search_games_by_title(self, search_query: str) -> list:
        games = self._session_cm.session.query(Game).filter(
            Game._Game__game_title.ilike(f"%{search_query}%")
        ).all()
        return games

    def search_games_by_genre(self, search_query: str) -> list:
        games = self._session_cm.session.query(Game).filter(
            Game._Game__genres.any(Genre._Genre__genre_name.ilike(f"%{search_query}%"))
        ).all()
        return games

    def search_games_by_publisher(self, search_query: str) -> list:
        games = self._session_cm.session.query(Game).filter(
            Game._Game__publisher.has(Publisher._Publisher__publisher_name.ilike(f"%{search_query}%"))
        ).all()
        return games

    def update_game(self, game: Game):
        if isinstance(game, Game):
            with self._session_cm as scm:
                scm.session.merge(game)
                scm.commit()

    def update_user(self, user: User):
        if isinstance(user, User):
            with self._session_cm as scm:
                scm.session.merge(user)
                scm.commit()
