from models import db, User, Movie

class DataManager():
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        """Returns a list of all users in the database."""
        return User.query.all()

    def get_movies(self, user_id):
        """Returns a list of all movies for a specific user."""
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} does not exist.")
        return user.movies

    def add_movie(self, title, director, year, poster_url, user_id):
        """Adds a new movie to a user's favorites."""
        new_movie = Movie(
            title=title,
            director=director,
            year=year,
            poster_url=poster_url,
            user_id=user_id
        )
        db.session.add(new_movie)
        db.session.commit()

    def update_movie(self, movie_id, title=None, director=None, year=None, poster_url=None):
        """Updates movie details."""
        movie = Movie.query.get(movie_id)
        if movie:
            if title: movie.title = title
            if director: movie.director = director
            if year: movie.year = year
            if poster_url: movie.poster_url = poster_url
            db.session.commit()

    def delete_movie(self, movie_id):
        """Removes a movie from the database."""
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False

    def get_user_by_id(self, user_id):
        """Fetches a single user by their ID, returns None if not found."""
        return db.session.get(User, user_id)

    def get_movie_by_id(self, movie_id):
        return db.session.get(Movie, movie_id)
