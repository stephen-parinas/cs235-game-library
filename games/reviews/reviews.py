from datetime import datetime

from flask import Blueprint, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import HiddenField, RadioField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

from games.authentication.authentication import login_required
from games.reviews import services
import games.adapters.repository as repo

# Configure blueprint
reviews_blueprint = Blueprint('reviews_bp', __name__)


@reviews_blueprint.route('/reviews/add_review', methods=['POST'])
@login_required
def add_review():
    form = ReviewForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        game_id = int(form.game_id.data)
        rating = 6 - int(form.rating.data)
        comment = form.comment.data
        current_datetime = str(datetime.now())
        services.add_new_review(repo.repo_instance, username, game_id, rating, comment, current_datetime)
        return redirect(url_for('info_bp.get_game_info', game_id=game_id))


class ReviewForm(FlaskForm):
    username = HiddenField('Username', validators=[DataRequired()])
    game_id = HiddenField('Game ID', validators=[DataRequired()])
    rating = RadioField(
        'Rating',
        choices=[('1', '☆'), ('2', '☆'), ('3', '☆'), ('4', '☆'), ('5', '☆')],
        validators=[DataRequired()]
    )
    comment = TextAreaField('Comment')
    submit = SubmitField('Submit')


