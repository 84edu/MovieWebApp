from flask import Flask, render_template, request, redirect, url_for, flash
from data_manager import DataManager
from models import db, Movie, User
from dotenv import load_dotenv
import os
import requests

load_dotenv()
app = Flask(__name__)

OMDB_API_KEY = os.getenv('API_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()

@app.route('/users', methods=['POST'])
def create_user():
    user_name = request.form.get('name')
    if user_name:
        data_manager.create_user(user_name)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def user_movies(user_id):
    if request.method == 'POST':
        movie_title = request.form.get('title')
        # OMDb API Call
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data.get('Response') == 'True':
            data_manager.add_movie(
                title=data.get('Title'),
                director=data.get('Director'),
                year=data.get('Year')[:4],
                poster_url=data.get('Poster'),
                user_id=user_id
            )
        return redirect(url_for('user_movies', user_id=user_id))

    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    new_title = request.form.get('title')
    data_manager.update_movie(movie_id, new_title)
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/')
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run()
