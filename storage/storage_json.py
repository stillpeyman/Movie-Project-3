from storage.istorage import IStorage
import json
import os


class StorageJson(IStorage):
    def __init__(self, filename):
        """
        Initialize the storage by setting the JSON file path inside the data folder.
        Creates an empty file if it doesn't exist.
        """
        # Get the folder path where <storage_json.py> is located
        base_dir = os.path.dirname(__file__)
        # Go up from </storage> folder (".."), then go into the data/ folder
        data_dir = os.path.abspath(os.path.join(base_dir, "..", "data"))

        # Only use basename to avoid double directory, e.g. 'data'
        filename = os.path.basename(filename)

        self._file_path = os.path.join(data_dir, filename)
        # print(f"Looking for file at: {self._file_path}")

        # If file doesn't exist, create empty JSON file
        if not os.path.exists(self._file_path):
            self._create_empty_file()


    def _create_empty_file(self):
        """
        Create an empty JSON file if it doesn't exist.
        """
        # <os.makedirs> – Create dir (and necessary parent dirs) unless already existing
        # <os.path.dirname> – gets dir part of the file path (~/.../250411_CODIO_Movie_Phase_3/data)
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        with open(self._file_path, "w", encoding="utf-8") as handle:
            json.dump({}, handle, indent=4)


    def _save_to_file(self, movies):
        """
        Private method to write the updated movies dictionary back to the file.
        """
        with open(self._file_path, "w", encoding="utf-8") as handle:
            json.dump(movies, handle, indent=4)


    def list_movies(self):
        """
        Return all movies stored in the JSON file.

        Returns:
            dict: A dictionary of movie titles and
            their associated information (year, rating, poster).
        """
        if not os.path.exists(self._file_path):
            # If file doesn't exist, return empty dict
            return {}

        with open(self._file_path, "r", encoding="utf-8") as handle:
            try:
                movies = json.load(handle)

            except json.JSONDecodeError:
                # If file is empty or contains invalid JSON, return empty dict
                movies = {}

        return movies


    def movie_exist(self, title):
        """
        Check if a movie with the given title already exists in storage.

        Args:
            title (str): The title of the movie to check.

        Returns:
            bool: True if the movie exists, otherwise False.
        """
        movies = self.list_movies()
        return title in movies


    def add_movie(self, title, year, rating, poster, imdb_id):
        """
        Add a new movie to the storage if it doesn't already exist.

        Args:
            title (str): The title of the movie.
            year (int): The year the movie was released.
            rating (str): The movie's rating.
            poster (str): The URL to the movie's poster image.
            imdb_id (str): imdbID of a movie title.
        """
        movies = self.list_movies()

        if not self.movie_exist(title):
            movies[title] = {
                "year": year,
                "rating": rating,
                "poster": poster,
                "imdb_id": imdb_id,
                "notes": ""
            }

        else:
            print(f"Movie '{title}' already exists.")

        self._save_to_file(movies)


    def delete_movie(self, title):
        """
        Delete a movie from the storage by its title.

        Args:
            title (str): The title of the movie to delete.
        """
        movies = self.list_movies()

        if not self.movie_exist(title):
            print(f"Movie '{title}' not found.")
        else:
            del movies[title]
            print(f"Movie {title} successfully deleted")

        self._save_to_file(movies)


    def update_movie(self, title, rating, notes):
        """
        Update the rating of an existing movie in the storage.
        Add movies notes to an existing movie in the storage.

        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating of the movie.
            notes (str): movie notes.
        """
        movies = self.list_movies()

        if not self.movie_exist(title):
            print(f"Movie '{title}' not found.")
        else:
            movies[title].update({"rating": rating})
            movies[title] ["notes"] = notes

        self._save_to_file(movies)
