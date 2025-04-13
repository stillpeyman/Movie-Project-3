from istorage import IStorage
import csv
import os


class StorageCsv(IStorage):
    def __init__(self, file_path):
        """
        Initialize the storage with the given file path.

        Args:
            file_path (str): Path to the CSV file storing movie data.
        """
        self._file_path = file_path

        # If file doesn't exist, create empty CSV file
        if not os.path.exists(self._file_path):
            self._create_empty_file()


    def _create_empty_file(self):
        """
        Create an empty CSV file if it doesn't exist.
        """
        with open(self._file_path, "w", encoding="utf-8") as handle:
            fieldnames = ["title", "year", "rating", "poster"]
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
                "poster": info["poster"]
            }
            rows.append(row)

        with open(self._file_path, "w", encoding="utf-8") as handle:
            fieldnames = ["title", "year", "rating", "poster"]
            writer = csv.DictWriter(handle, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(rows)


    def list_movies(self):
        """
        List all movies stored in the CSV file.

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
                        "poster": row["poster"]
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
        if title in movies:
            print(f"Movie {title} already exists.")
            return True
        return False


    def add_movie(self, title, year, rating, poster):
        """
        Add a new movie to the storage.

        Args:
            title (str): The title of the movie.
            year (int): The year the movie was released.
            rating (float): The movie's rating.
            poster (str): The URL to the movie's poster image.
        """
        movies = self.list_movies()

        if not self.movie_exist(title):
            movies[title] = {"year": year, "rating": rating, "poster": poster}
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

        if self.movie_exist(title):
            del movies[title]
        else:
            print(f"Movie '{title}' not found.")

        self._save_to_file(movies)


    def update_movie(self, title, rating):
        """
        Update the rating of an existing movie in the storage.

        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating of the movie.
        """
        movies = self.list_movies()

        if self.movie_exist(title):
            movies[title].update({"rating": rating})
        else:
            print(f"Movie '{title}' not found.")

        self._save_to_file(movies)
