import pytest

from flask import session


# authentication blueprint
def test_register(client):
    # Check that the register page is retrieved
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that a user is registered successfully
    response = client.post(
        '/authentication/register',
        data={'user_name': 'baekhyunbyun', 'password': 'Passw0rd2'}
    )
    assert response.headers['Location'] == '/authentication/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('mk', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 7 characters\n, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('marklee', 'Passw0rd', b'Your username is already taken, please try again.'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid username/password generate the right error message
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    response_code = client.get('/authentication/login').status_code
    assert response_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == '/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'marklee'

    # Check that 'sign in' button has changed to 'sign out'
    response = client.get('/')
    assert response.status_code == 200
    assert b'SIGN OUT' in response.data
    assert b'SIGN IN' not in response.data


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('test', '', b'Your password is required'),
        ('taylorswift', 'Passw0rd', b'User name not recognised, try again.'),
        ('marklee', 'Password', b'Password does not match with user name, try again.'),
))
def test_login_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid username/password generate the right error message
    response = client.post(
        '/authentication/login',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_logout(client, auth):
    # Login a user.
    auth.login()

    # Check that a successful logout generates a redirect to the homepage.
    response = auth.logout()
    assert response.headers['Location'] == '/'

    # Check that logging out clears the user's session.
    with client:
        client.get('/')
        assert 'user_name' not in session

    # Check that 'sign out' button has changed to 'sign in'
    response = client.get('/')
    assert response.status_code == 200
    assert b'SIGN OUT' not in response.data
    assert b'SIGN IN' in response.data


# allgames blueprint
def test_show_all_games(client):
    # Check that the allgames page can be retrieved (default, first page)
    response = client.get('/all_games')
    assert response.status_code == 200
    assert b"Browse All Games" in response.data

    # Check pagination tabs for first page
    assert b"First" not in response.data
    assert b"Previous" not in response.data
    assert b"Page 1" in response.data
    assert b"Next" in response.data
    assert b"Last" in response.data

    # Check that the max number of allowed games is shown
    count = response.data.count(b'<div class="game">')
    assert count == 16

    # Check the last page can be retrieved
    response = client.get('/all_games/2')
    assert response.status_code == 200

    # Check pagination tabs for last page
    assert b"First" in response.data
    assert b"Previous" in response.data
    assert b"Page 2" in response.data
    assert b"Next" not in response.data
    assert b"Last" not in response.data

    # Check that the correct number of remaining games is shown
    count = response.data.count(b'<div class="game">')
    assert count == 3


# home blueprint
def test_home(client):
    # Check that the home page can be retrieved
    response = client.get('/')
    assert response.status_code == 200
    assert b"Our game library website" in response.data

    # Check that the correct number of recently added games is shown
    count = response.data.count(b'<div class="game">')
    assert count == 4

    # Check that the correct number of popular action games is shown
    count = response.data.count(b'<div class="game1">')
    assert count == 4


# info blueprint
def test_get_game_info(client):
    # Check that the game info page can be retrieved
    response = client.get('/info/1995240')
    assert b"Deer Journey" in response.data
    assert response.status_code == 200

    # Check that game with more than 3 reviews shows reviews and the 'view reviews' button
    assert b"marklee" in response.data
    assert b"View all reviews" in response.data

    # Check that game with 3 or less reviews shows reviews but not the 'view reviews' button
    response = client.get('/info/316260')
    assert response.status_code == 200
    assert b"oliviarodrigo" in response.data
    assert b"View all reviews" not in response.data

    # Check that game with no reviews has the appropriate message
    response = client.get('/info/730310')
    assert response.status_code == 200
    assert b"This game has no reviews" in response.data
    assert b"View all reviews" not in response.data

    # Check that up to 5 recommended games are shown
    count = response.data.count(b'<div class="rec-game">')
    assert count <= 5


# profile blueprint
def test_add_to_favourites(client, auth):
    # Login a user
    auth.login()

    # Check that the game info page is retrieved
    response = client.get('/info/316260')
    assert b"Disney Universe" in response.data
    assert response.status_code == 200
    assert b"Add to favourites" in response.data
    assert b"Added to favourites" not in response.data

    # Add game to favourites
    response = client.post('/add_to_favourites/316260')
    assert response.status_code == 302
    assert response.headers['Location'] == '/info/316260'

    # Check that button is updated
    response = client.get('/info/316260')
    assert response.status_code == 200
    assert b"Add to favourites" not in response.data
    assert b"Added to favourites" in response.data


def test_remove_from_favourites(client, auth):
    # Login a user
    auth.login()

    # Check that the game info page is retrieved
    client.post('/add_to_favourites/316260')
    response = client.get('/info/316260')
    assert b"Disney Universe" in response.data
    assert response.status_code == 200
    assert b"Add to favourites" not in response.data
    assert b"Added to favourites" in response.data

    # Remove game from favourites
    response = client.post('/remove_from_favourites/316260')
    assert response.status_code == 302
    assert response.headers['Location'] == '/info/316260'

    # Check that button is updated
    response = client.get('/info/316260')
    assert response.status_code == 200
    assert b"Add to favourites" in response.data
    assert b"Added to favourites" not in response.data


def test_show_profile(client, auth):
    # Login a user
    auth.login()

    # Check that the profile page is retrieved
    pass


# review blueprint
def test_add_review(client, auth):
    # Login a user
    auth.login()

    # Check that the game info page is retrieved
    response = client.get('/info/316260')
    assert b"Disney Universe" in response.data
    assert response.status_code == 200

    # Check that review button is retrieved
    assert b"Add a review" in response.data

    # Add a review
    response = client.post(
        '/reviews/add_review',
        data={'username': 'marklee', 'game_id': 316260, 'rating': 5, 'comment': 'Great game!'}
    )
    assert response.status_code == 302
    assert response.headers['Location'] == '/info/316260'

    # Check that review is now on the page
    response = client.get('/info/316260')
    assert response.status_code == 200
    assert b"marklee" in response.data
    assert b"Great game!" in response.data


def test_login_required(client):
    # Test the pages that require login
    response = client.post('/reviews/add_review')
    assert response.headers['Location'] == '/authentication/login'
    response = client.post('/add_to_favourites/316260')
    assert response.headers['Location'] == '/authentication/login'
    response = client.post('/remove_from_favourites/316260')
    assert response.headers['Location'] == '/authentication/login'
    response = client.get('/profile')
    assert response.headers['Location'] == '/authentication/login'


# sidebar blueprint
def test_search(client):
    # Test that searching obtains the correct page and number of games

    # Searching by title
    response = client.get('/search/?filter=title&query=th')
    assert response.status_code == 200
    assert b'Search results for: th' in response.data
    count = response.data.count(b'<div class="game">')
    assert count == 6

    # Searching by genre
    response = client.get('/search/?filter=genre&query=ad')
    assert response.status_code == 200
    assert b'Search results for: ad' in response.data
    count = response.data.count(b'<div class="game">')
    assert count == 4

    # Searching by genre
    response = client.get('/search/?filter=publisher&query=ad')
    assert response.status_code == 200
    assert b'Search results for: ad' in response.data
    count = response.data.count(b'<div class="game">')
    assert count == 2


def test_games_by_genre(client):
    # Test that filtering obtains the correct page and number of games
    response = client.get('/games_by_genre?genre=Adventure')
    assert response.status_code == 200
    assert b'Adventure' in response.data
    count = response.data.count(b'<div class="game">')
    assert count == 4


def test_games_by_publisher(client):
    # Test that filtering obtains the correct page and number of games
    response = client.get('/games_by_publisher?publisher=Disney')
    assert response.status_code == 200
    assert b'Disney' in response.data
    count = response.data.count(b'<div class="game">')
    assert count == 1
