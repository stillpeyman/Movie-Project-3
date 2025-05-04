from abc import ABC, abstractmethod


class IStorage(ABC):
    """
   Abstract base class for movie storage.

   This class defines the methods required for managing a collection of movies,
   including listing, adding, deleting, updating, and checking the existence of movies.
   Child classes must implement these methods to interact with the underlying storage
   (e.g., a database or file system).
   """

    @abstractmethod
    def list_movies(self):
        """
        List all movies in the storage.

        Returns:
            dict: A dictionary where the keys are movie titles and the values are dictionaries
                  containing movie details such as year, rating, and poster.
        """
        pass


    @abstractmethod
    def movie_exist(self, title):
        """
        Check if a movie exists in the storage.

        Args:
            title (str): The title of the movie to check.

        Returns:
            bool: True if the movie exists, otherwise False.
        """
        pass


    @abstractmethod
    def add_movie(self, title, year, rating, poster, imdb_id):
        """
        Add a new movie to the storage.

        Args:
            title (str): The title of the movie.
            year (int): The release year of the movie.
            rating (str): The rating of the movie.
            poster (str): The URL of the movie's poster image.
            imdb_id (str): imdbID of a movie title
        """
        pass


    @abstractmethod
    def delete_movie(self, title):
        """
        Delete a movie from the storage.

        Args:
            title (str): The title of the movie to delete.
        """
        pass


    @abstractmethod
    def update_movie(self, title, rating, notes):
        """
        Update the rating of an existing movie in the storage.

        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating for the movie.
            notes (str): movie notes.
        """
        pass


