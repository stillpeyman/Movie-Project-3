from storage.istorage import IStorage
import csv
import os


class StorageCsv(IStorage):
    def __init__(self, filename):
        """
        Initialize the storage by setting the CSV file path inside the data folder.
        Creates an empty file if it doesn't exist.
        """
        base_dir = os.path.dirname(__file__)
        data_dir = os.path.abspath(os.path.join(base_dir, "..", "data"))

        filename = os.path.basename(filename)

        self._file_path = os.path.join(data_dir, filename)

        # If file doesn't exist, create empty CSV file
        if not os.path.exists(self._file_path):
            self._create_empty_file()


    def _create_empty_file(self):
        """
        Create an empty CSV file if it doesn't exist.
        """
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        with open(self._file_path, "w", encoding="utf-8") as handle:
            # <fieldnames> represent the column headers in CSV file
            fieldnames = ["title", "year", "rating", "poster", "imdb_id", "notes"]
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()


    def _save_to_file(self, movies):
        """
        Private method to write the updated movies dictionary back to the file.
        """
        rows = []
        for title, info in movies.items():
            row = {
                "title": title,
                "year": info["year"],
                "rating": info["rating"],
                "poster": info["poster"],
                "imdb_id": info["imdb_id"],
                "notes": info["notes"]
            }
            rows.append(row)

        with open(self._file_path, "w", encoding="utf-8") as handle:
            fieldnames = ["title", "year", "rating", "poster", "imdb_id", "notes"]
            writer = csv.DictWriter(handle, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(rows)


    def list_movies(self):
        """
        Return all movies stored in the CSV file.

        Returns:
            dict: A dictionary of movie titles and
            their associated information (year, rating, poster).
        """
        # Initialise movies dict
        movies = {}

        if not os.path.exists(self._file_path):
            # If file doesn't exist, return empty dict
            return movies
        try:
            with open(self._file_path, "r", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                for row in reader:
                    title = row["title"]
                    movies[title] = {
                        "year": row["year"],
                        "rating": row["rating"],
                        "poster": row["poster"],
                        "imdb_id": row["imdb_id"],
                        "notes": row["notes"]
                    }
        except csv.Error as e:
            print(f"Error reading CSV file: {e}")
            # Return empty dict in case of CSV error
            return movies

        except Exception as e:
            print(f"Unexpected error: {e}")
            # Return empty dict in case of any unexpected error
            return movies

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

        self._save_to_file(movies)


    def update_movie(self, title, rating, notes):
        """
        Update the rating of an existing movie in the storage.

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
