from sqlalchemy import select, inspect
from games.adapters.orm import metadata


def testing_db_inspect_table_names(database_engine):
    inspecting = inspect(database_engine)
    print(inspecting.get_table_names())
    assert inspecting.get_table_names() == ['favourites', 'game_genres', 'games', 'genres', 'publishers',
                                            'recommended_games', 'reviews', 'users']


def test_database_populates_all_favourites(database_engine):
    inspecting = inspect(database_engine)
    name_games_table = inspecting.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_games_table]])
        result = connection.execute(select_statement)

        all_favourites = []
        for row in result:
            all_favourites.append((row['user_name'], row['game_id']))
        assert all(fav in all_favourites for fav in [("oliviarodrigo", 410320), ("oliviarodrigo", 730310)])


def test_database_populates_all_game_genres(database_engine):
    inspecting = inspect(database_engine)
    name_games_table = inspecting.get_table_names()[1]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_games_table]])
        result = connection.execute(select_statement)

        all_game_genres = []
        for row in result:
            all_game_genres.append((row['game_id'], row['genre_name']))
        assert all(gg in all_game_genres for gg in [(12140, "Action"),
                                                    (22670, "Action"),
                                                    (34282, "Action"),
                                                    (45750, "Action"),
                                                    (45750, "Adventure"),
                                                    (242530, "Action"),
                                                    (267360, "Action"),
                                                    (311120, "Action"),
                                                    (316260, "Action"),
                                                    (316260, "Adventure"),
                                                    (410320, "Action"),
                                                    (418650, "Action"),
                                                    (465070, "Action"),
                                                    (730310, "Action"),
                                                    (781240, "Action"),
                                                    (944590, "Action"),
                                                    (1271620, "Action"),
                                                    (1581010, "Action"),
                                                    (1581010, "Adventure"),
                                                    (1875470, "Action"),
                                                    (1995240, "Adventure"),
                                                    (1995240, "Indie"),
                                                    (1998840, "Action")])


def test_database_populates_all_games(database_engine):
    inspecting = inspect(database_engine)
    name_games_table = inspecting.get_table_names()[2]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_games_table]])
        result = connection.execute(select_statement)

        all_games = []
        for row in result:
            all_games.append((row['game_id'], row['game_title']))
        all_games = sorted(all_games, key=lambda x: x[0])
        assert all_games == [(12140, "Max Payne"),
                             (22670, "Alien Breed 3: Descent"),
                             (34282, "Shadow Dancer™"),
                             (45750, "Lost Planet® 2"),
                             (242530, "The Chaos Engine"),
                             (267360, "MURI"),
                             (311120, "The Stalin Subway: Red Veil"),
                             (316260, "Disney Universe"),
                             (410320, "EARTH DEFENSE FORCE 4.1 The Shadow of New Despair"),
                             (418650, "Space Pirate Trainer"),
                             (465070, "TRIZEAL Remix"),
                             (730310, "DYNASTY WARRIORS 9"),
                             (781240, "Mystical"),
                             (944590, "Thunder Kid"),
                             (1271620, "Umihara Kawase BaZooKa!"),
                             (1581010, "Haunted House - The Murder"),
                             (1875470, "Ninjas Against the Machines"),
                             (1995240, "Deer Journey"),
                             (1998840, "Arcadia")]


def test_database_populates_all_genres(database_engine):
    inspecting = inspect(database_engine)
    name_genre_table = inspecting.get_table_names()[3]
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_genre_table]])
        result = connection.execute(select_statement)

        all_genres = []
        for row in result:
            all_genres.append(row['genre_name'])
        all_genres.sort()
        assert all_genres == ['Action', 'Adventure', 'Indie']


def test_database_populates_all_publishers(database_engine):
    inspecting = inspect(database_engine)
    name_publisher_table = inspecting.get_table_names()[4]
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_publisher_table]])
        result = connection.execute(select_statement)

        all_publishers = []
        for row in result:
            all_publishers.append(row['name'])
        all_publishers.sort()
        assert all_publishers == ["Buka Entertainment", "Capcom", "D3PUBLISHER", "Deadcloud Productions", "Disney",
                                  "I-Illusions", "KOEI TECMO GAMES CO., LTD.", "Komodo", "Ludosity", "Ome6a Games",
                                  "Pablo Picazo", "Pixel Games UK", "Rebellion", "Renegade Sector Games",
                                  "Rockstar Games", "SEGA", "SUCCESS Corp.", "Team17 Digital Ltd", "Ziggurat"]


def test_database_populates_all_recommended_games(database_engine):
    # this doesn't actually get populated until you open the game info page, at which it will determine similar games
    pass


def test_database_populates_all_reviews(database_engine):
    inspecting = inspect(database_engine)
    name_reviews_table = inspecting.get_table_names()[6]
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append((row['user_name'], row['game_id'], row['rating'], row['review_text']))
        assert all(
            review in all_reviews for review in [("oliviarodrigo", 316260, 5, 'five'), ("marklee", 1995240, 5, 'five'),
                                                 ("marklee", 1995240, 4, 'four'), ("marklee", 1995240, 3, 'three'),
                                                 ("marklee", 1995240, 2, 'two'), ("marklee", 1995240, 1, 'one')])


def test_database_populates_all_users(database_engine):
    inspecting = inspect(database_engine)
    name_users_table = inspecting.get_table_names()[7]
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append((row['user_name']))
        all_users.sort()
        assert all_users == ["marklee", "oliviarodrigo"]
