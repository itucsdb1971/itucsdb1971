import psycopg2 as dbapi2

from movie import Movie


class Database:
    def __init__(self, db_url):
        self.db_url = db_url

    def add_movie(self, movie):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO movie (title, yr) VALUES (%s, %s) RETURNING id"
            cursor.execute(query, (movie.title, movie.year))
            connection.commit()
            movie_key, = cursor.fetchone()
        return movie_key

    def update_movie(self, movie_key, movie):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "UPDATE movie SET title = %s, yr = %s WHERE (id = %s)"
            cursor.execute(query, (movie.title, movie.year, movie_key))
            connection.commit()

    def delete_movie(self, movie_key):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM movie WHERE (id = %s)"
            cursor.execute(query, (movie_key,))
            connection.commit()

    def get_movie(self, movie_key):
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT title, yr FROM movie WHERE (id = %s)"
            cursor.execute(query, (movie_key,))
            try:
                title, year = cursor.fetchone()
            except TypeError:
                return None
        movie_ = Movie(title, year=year)
        return movie_

    def get_movies(self):
        movies = []
        with dbapi2.connect(self.db_url) as connection:
            cursor = connection.cursor()
            query = "SELECT id, title, yr FROM movie ORDER BY id"
            cursor.execute(query)
            for movie_key, title, year in cursor:
                movies.append((movie_key, Movie(title, year)))
        print(movies)
        return movies
