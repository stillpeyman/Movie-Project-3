import random
from fuzzywuzzy import process
import datetime
import omdb_api


class MovieApp:
    def __init__(self, json_storage, csv_storage):
        """
        Initialize the MovieApp with a given storage.
        """
        self._json_storage = json_storage
        self._csv_storage = csv_storage


    def _command_list_movies(self):
        """
        List all movies stored in the app
        with their title, year, and rating.
        """
        movies = self._json_storage.list_movies()
        print(f"{len(movies)} movies in total:")
        for title, info in movies.items():
            print(f"{title} ({info['year']}): {info['rating']}")


    def _command_add_movie(self):
        """
        Prompt user to input details for a
        new movie and adds it to the storage.
        """
        while True:
            new_title = input("Enter new movie name (or 'q' to cancel): ").title()

            if new_title.lower() == 'q':
                print("Action cancelled.")
                return

            # check if title is empty string
            if not new_title.strip():
                print("Invalid input! Title cannot be empty.")
                continue

            if self._json_storage.movie_exist(new_title):
                continue

            try:
                movie_json = omdb_api.get_json(new_title)
                movie_csv = omdb_api.get_csv(new_title)
                break

            except ValueError as e:
                print(f"{str(e)}")
                continue

        self._json_storage.add_movie(movie_json["Title"], movie_json["Year"], movie_json["imdbRating"], movie_json["Poster"])
        self._csv_storage.add_movie(movie_csv["Title"], movie_csv["Year"], movie_csv["imdbRating"], movie_csv["Poster"])
        print(f"Movie {new_title} successfully added")


    def _command_delete_movie(self):
        """
        Prompt user to enter a movie title
        to delete from storage.
        """
        while True:
            title = input("Enter movie name to delete (or 'q' to cancel): ").title()

            if title.lower() == "q":
                print("Action cancelled.")
                return

            # check if title is empty string
            if not title.strip():
                print("Invalid input! Title cannot be empty.")
                continue

            self._json_storage.delete_movie(title)
            self._csv_storage.delete_movie(title)
            break


    def _command_update_movie(self):
        """
        Prompt user to update the rating of an existing movie.
        """
        while True:
            title = input("Enter movie name (or 'q' to cancel): ").title()

            if title.lower() == "q":
                print("Action cancelled.")
                return

            # check if title is empty string
            if not title.strip():
                print("Invalid input! Title cannot be empty.")
                continue

            if not self._json_storage.movie_exist(title):
                continue

            else:
                break

        while True:
            try:
                rating = input("Enter new movie rating between 0 and 10 (or 'q' to cancel): ")

                if rating.lower() == "q":
                    print("Action cancelled.")
                    return

                new_rating = float(rating.replace(",", "."))
                if not 0 <= new_rating <= 10:
                    print(f"Invalid rating! Please enter a number between 0 and 10.")
                    continue

                self._json_storage.update_movie(title, new_rating)
                self._csv_storage.update_movie(title, new_rating)
                print(f"Movie {title} successfully updated")
                break

            except ValueError:
                print("Invalid rating! Please enter a number between 0 and 10.")


    def _command_movie_stats(self):
        """
        Display statistics for all movies,
        including average, median, best,
        and worst ratings.
        """
        movies = self._json_storage.list_movies()

        sorted_ratings = sorted(info["rating"] for info in movies.values())

        average_rating = sum(sorted_ratings) / len(sorted_ratings)
        print(f"Average rating: {round(average_rating, 2)}")

        ratings_count = len(sorted_ratings)
        mid_index = ratings_count // 2

        if ratings_count % 2 == 0:
            median_rating = (sorted_ratings[mid_index - 1] + sorted_ratings[mid_index]) / 2
        else:
            median_rating = sorted_ratings[mid_index]

        print(f"Median rating: {median_rating}")

        best_rating = max(info["rating"] for info in movies.values())
        best_movies = [title for title, info in movies.items() if info["rating"] == best_rating]

        if len(best_movies) == 1:
            print(f"Best movie: {best_movies[0]}, {best_rating}")
        else:
            print(f"Best movies: {', '.join(best_movies)}, {best_rating}")

        worst_rating = min(info["rating"] for info in movies.values())
        worst_movies = [title for title, info in movies.items() if
                        info["rating"] == worst_rating]

        if len(worst_movies) == 1:
            print(f"Worst movie: {worst_movies[0]}, {worst_rating}")
        else:
            print(f"Worst movies: {', '.join(worst_movies)}, {worst_rating}")


    def _command_get_random_movie(self):
        """
        Suggest a random movie from the storage for the user to watch.
        """
        movies = self._json_storage.list_movies()

        database_tuple_ls = list(movies.items())
        random_selection = random.choice(database_tuple_ls)
        print(f"Your movie for tonight: {random_selection[0]}, it's rated {random_selection[1]['rating']}.")


    def _command_search_movie(self):
        """
        Search for movies based on a partial
        name using fuzzy string matching.
        """
        movies = self._json_storage.list_movies()

        while True:
            title = input("Enter part of the movie name (or 'q' to cancel): ").casefold()

            if title.lower() == "q":
                print("Action cancelled.")
                return

            # check for empty string
            if not title.strip():
                print("Invalid input! Title cannot be empty.")
                continue

            break

        # fuzzymatch module: using process.extract() to get best matches
        best_matches = process.extract(title, movies.keys(), limit=5)

        # manually filter matches based on score threshold
        filtered_matches = [(movie, score) for movie, score in best_matches if score >= 70]

        if filtered_matches:
            for movie, score in filtered_matches:
                print(f"{movie} ({movies[movie]['year']}): {movies[movie]['rating']}")

        else:
            print(f"No matches found")


    def _command_sort_movies_desc(self):
        """
        Sort and display all movies by their rating in descending order.
        """
        movies = self._json_storage.list_movies()

        sorted_movie_list = sorted(movies.items(), key=lambda item: item[1]["rating"], reverse=True)
        for movie in sorted_movie_list:
            print(f"{movie[0]}: {movie[1]['rating']}")


    def _generate_website(self):
        """
        Generate a website displaying the movie database.
        """
        pass


    def run(self):
        """
        Display the menu and handles user commands.
        """
        menu = """
        Menu: 
        0. Exit
        1. List Movies
        2. Add Movie
        3. Delete Movie
        4. Update Movie
        5. Stats
        6. Random Movie
        7. Search Movie
        8. Movies Sorted by rating
        9. Generate Website
        """

        user_choices = {
            "1": self._command_list_movies,
            "2": self._command_add_movie,
            "3": self._command_delete_movie,
            "4": self._command_update_movie,
            "5": self._command_movie_stats,
            "6": self._command_get_random_movie,
            "7": self._command_search_movie,
            "8": self._command_sort_movies_desc,
            "9": self._generate_website
        }

        while True:
            print(f"{10 * '*'} My Movies Database {10 * '*'}")
            print(menu)
            user_input = input("Enter choice (0-8): ").strip()
            # Ignore empty input
            if not user_input:
                continue

            if user_input == "0":
                print("Bye!")
                break

            if user_input in user_choices:
                # basically calling the function with <movies> as arg
                user_choices[user_input]()
                input("\nPress enter to continue")

            else:
                print("Invalid choice")
                continue