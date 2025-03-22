import csv
import os

from games.domainmodel.model import Genre, Game, Publisher, User, Review


class GameFileCSVReader:
    def __init__(self, game_filename, user_filename = ""):
        self.__game_filename = game_filename
        self.__dataset_of_games = []
        self.__dataset_of_publishers = set()
        self.__dataset_of_genres = set()
        self.__user_filename = user_filename
        self.__dataset_of_users = set()

    def read_game_csv_file(self):
        if not os.path.exists(self.__game_filename):
            print(f"path {self.__game_filename} does not exist!")
            return
        with open(self.__game_filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    game_id = int(row["AppID"])
                    title = row["Name"]
                    game = Game(game_id, title)
                    game.release_date = row["Release date"]
                    game.price = float(row["Price"])
                    game.description = row["About the game"]
                    game.image_url = row["Header image"]
                    if row["Movies"]:
                        game.trailer_url = row["Movies"].split(',')[0]
                    else:
                        game.trailer_url = row["Screenshots"].split(',')[0]

                    publisher = Publisher(row["Publishers"])
                    self.__dataset_of_publishers.add(publisher)
                    game.publisher = publisher

                    genre_names = row["Genres"].split(",")
                    for genre_name in genre_names:
                        genre = Genre(genre_name.strip())
                        self.__dataset_of_genres.add(genre)
                        game.add_genre(genre)

                    self.__dataset_of_games.append(game)

                except ValueError as e:
                    print(f"Skipping row due to invalid data: {e}")
                except KeyError as e:
                    print(f"Skipping row due to missing key: {e}")

    def get_unique_games_count(self):
        return len(self.__dataset_of_games)

    def get_unique_genres_count(self):
        return len(self.__dataset_of_genres)

    def get_unique_publishers_count(self):
        return len(self.__dataset_of_publishers)

    @property
    def dataset_of_games(self) -> list:
        return self.__dataset_of_games

    @property
    def dataset_of_publishers(self) -> set:
        return self.__dataset_of_publishers

    @property
    def dataset_of_genres(self) -> set:
        return self.__dataset_of_genres

    def read_user_csv_file(self):
        if not os.path.exists(self.__user_filename):
            print(f"path {self.__user_filename} does not exist!")
            return
        with open(self.__user_filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    username = row["Username"]
                    password = row["Password"]
                    user = User(username, password)

                    review_data = (row["Reviews"]).split('|')
                    if review_data[0] != '':
                        for review in review_data:
                            components = review.split(',')
                            game = next(game for game in self.__dataset_of_games if game.game_id == int(components[0]))
                            review = Review(user, game, int(components[2]), components[3], components[4])
                            user.add_review(review)

                    favourites_data = (row["Favourites"]).split('|')
                    if favourites_data[0] != '':
                        for fav in favourites_data:
                            game = next(game for game in self.__dataset_of_games if game.game_id == int(fav))
                            user.add_favourite_game(game)

                    self.__dataset_of_users.add(user)

                except ValueError as e:
                    print(f"Skipping row due to invalid data: {e}")
                except KeyError as e:
                    print(f"Skipping row due to missing key: {e}")

    @property
    def dataset_of_users(self) -> set:
        return self.__dataset_of_users

    """def write_user_csv_file(self):
        if not os.path.exists(self.__user_filename):
            print(f"path {self.__user_filename} does not exist!")
            return
        with open(self.__user_filename, 'w', newline='') as file:
            fieldnames = ['Username', 'Password', 'Reviews', 'Favourites']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for user in self.__dataset_of_users:
                user_dict = {
                    'Username': user.username,
                    'Password': user.password,
                    'Reviews': '|'.join([f'{review.game.game_id}, {review.game.title}, {review.rating}, {review.comment}, {review.date}' for review in user.reviews]),
                    'Favourites': '|'.join([f'{game.game_id}, {game.title}' for game in user.favourite_games]),
                }
                writer.writerow(user_dict)"""
