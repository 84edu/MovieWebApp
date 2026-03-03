from flask import abort, Flask, render_template, request, redirect, url_for, flash
from data_manager import DataManager
from models import db, Movie, User
from dotenv import load_dotenv
import os
import requests

load_dotenv()
app = Flask(__name__)

OMDB_API_KEY = os.getenv('API_KEY')

if not OMDB_API_KEY:
    raise ValueError("No API_KEY found in environment variables!")

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()

@app.route('/users', methods=['POST'])
@app.route('/users/', methods=['POST'])
def create_user():
    user_name = request.form.get('name', '').strip()
    if user_name:
        data_manager.create_user(user_name)
        flash(f"User '{user_name}' created successfully!", "success")
    else:
        flash("User name cannot be empty!", "warning")

    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def user_movies(user_id):
    user = data_manager.get_user_by_id(user_id)

    if user is None:
        abort(404)

    if request.method == 'POST':
        movie_title = request.form.get('title')

        try:
            # 1. API Call with Timeout (to prevent hanging)
            url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
            response = requests.get(url, timeout=5)
            response.raise_for_status() # Raises an error for 4xx or 5xx responses
            data = response.json()

            if data.get('Response') == 'True':
                try:
                    # 2. Database interaction using your DataManager
                    data_manager.add_movie(
                        title=data.get('Title'),
                        director=data.get('Director'),
                        year=data.get('Year')[:4],
                        poster_url=data.get('Poster'),
                        user_id=user_id
                    )
                    flash(f"Movie '{data.get('Title')}' added successfully!", "success")
                except Exception as e:
                    # If DB fails, we must rollback to keep the session clean
                    db.session.rollback()
                    flash("An error occurred while saving to the database.", "danger")
                    print(f"Database Error: {e}")
            else:
                flash(f"Movie '{movie_title}' not found!", "warning")

        except requests.exceptions.RequestException as e:
            # Catching connection issues, timeouts, etc.
            flash("Could not connect to the movie database (OMDb). Please check your internet.", "danger")
            print(f"Connection Error: {e}")

        return redirect(url_for('user_movies', user_id=user_id))

    # GET logic stays simple but clean
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    movie = data_manager.get_movie_by_id(movie_id)

    if movie is None or movie.user_id != user_id:
        abort(404)

    new_title = request.form.get('title')
    if new_title:
        data_manager.update_movie(movie_id, new_title)
        flash("Movie title updated!", "success")

    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    movie = data_manager.get_movie_by_id(movie_id)

    if movie is None or movie.user_id != user_id:
        abort(404)

    try:
        data_manager.delete_movie(movie_id)
        flash("Movie was successfully deleted.", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while trying to delete the movie.", "danger")
        print(f"Delete Error: {e}")

    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/')
def index():
    """The only official URL for the user list."""
    users_list = data_manager.get_users()
    return render_template('index.html', users=users_list)

@app.route('/users', methods=['GET'])
@app.route('/users/', methods=['GET'])
def users_redirect():
    """SEO-friendly 301 Redirect to the root URL."""
    return redirect(url_for('index'), code=301)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run(debug=True)
