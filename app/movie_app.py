import random
from fuzzywuzzy import process
import api.omdb_api


class MovieApp:
    def __init__(self, data_storage):
        """
        Initialize the MovieApp with a given storage.
        """
        self._data_storage = data_storage


    def _command_list_movies(self):
        """
        List all movies stored in the app
        with their title, year, and rating.
        """
        movies = self._data_storage.list_movies()
        print(f"{len(movies)} movies in total:")
        for title, info in movies.items():
            notes = info.get("notes", "")
            print(f"{title} ({info['year']}): {info['rating']} | Notes: {notes}")


    def _command_add_movie(self):
        """
        Prompt user to input details for a
        new movie and adds it to the storage.
        """
        while True:
            user_input = input("Enter new movie name (or 'q' to cancel): ").title().strip()

            if user_input.lower() == 'q':
                print("Action cancelled.")
                return

            # check if title is empty string
            if not user_input.strip():
                print("Invalid input! Title cannot be empty.")
                continue

            if self._data_storage.movie_exist(user_input):
                print(f"Movie {user_input} already exists in database.")
                continue

            try:
                movie_data = api.omdb_api.get_movie_data(user_input)
                break

            # Catch ValueErrors from get_movie_data() in omdb_api.py
            except ValueError as e:
                print(f"{str(e)}")
                continue

            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                continue

        self._data_storage.add_movie(
            movie_data["Title"],
            movie_data["Year"],
            movie_data["imdbRating"],
            movie_data["Poster"],
            movie_data["imdbID"]
        )
        print(f"Movie {user_input} successfully added")


    def _command_delete_movie(self):
        """
        Prompt user to enter a movie title
        to delete from storage.
        """
        movies = self._data_storage.list_movies()

        while True:
            user_input = input("Enter part of the movie title (or 'q' to cancel): ").casefold().strip()

            if user_input.lower() == "q":
                print("Action cancelled.")
                return

            # check for empty string
            if not user_input.strip():
                print("Invalid input! Title cannot be empty.")
                continue

            # fuzzymatch module: using process.extract() to get best matches
            best_matches = process.extract(user_input, movies.keys(), limit=5)

            # manually filter matches based on score threshold
            filtered_matches = [(movie, score) for movie, score in best_matches if score >= 70]
            sorted_filtered_matches = sorted(filtered_matches, key=lambda item: item[1], reverse=True)

            if sorted_filtered_matches:
                for i in range(len(sorted_filtered_matches)):
                    print(f"{i + 1}. {sorted_filtered_matches[i][0]}")
                break

            else:
                print(f"No matches found, try again ...")
                continue

        while True:
            user_choice = input("\nEnter the number for the movie to delete (or 'q' to cancel): ").strip()

            if user_choice.lower() == "q":
                print("Action cancelled.")
                return

            # check if title is empty string
            if not user_choice.strip():
                print("Invalid input! Your choice cannot be empty.")
                continue

            if not user_choice.isdigit():
                print("Invalid input! Pick the number for the movie.")
                continue

            else:
                movie_to_delete = sorted_filtered_matches[int(user_choice) - 1][0]
                break

        self._data_storage.delete_movie(movie_to_delete)


    def _command_update_movie(self):
        """
        Prompt user to update the rating of an existing movie.
        """
        movies = self._data_storage.list_movies()
        movie_to_update = ""
        new_rating = ""
        movies_notes = ""

        while True:
            user_input = input("Enter part of the movie title (or 'q' to cancel): ").casefold().strip()

            if user_input.lower() == "q":
                print("Action cancelled.")
                return

            # check for empty string
            if not user_input.strip():
                print("Invalid input! Title cannot be empty.")
                continue

            # fuzzymatch module: using process.extract() to get best matches
            best_matches = process.extract(user_input, movies.keys(), limit=5)

            # manually filter matches based on score threshold
            filtered_matches = [(movie, score) for movie, score in best_matches if score >= 70]
            sorted_filtered_matches = sorted(filtered_matches, key=lambda item: item[1], reverse=True)

            if sorted_filtered_matches:
                for i in range(len(sorted_filtered_matches)):
                    print(f"{i + 1}. {sorted_filtered_matches[i][0]}")
                break

            else:
                print(f"No matches found, try again ...")
                continue

        while True:
            user_choice = input("\nEnter the number for the movie to update (or 'q' to cancel): ").strip()

            if user_choice.lower() == "q":
                print("Action cancelled.")
                return

            # check if title is empty string
            if not user_choice.strip():
                print("Invalid input! Your choice cannot be empty.")
                continue

            if not user_choice.isdigit():
                print("Invalid input! Pick the number for the movie.")
                continue

            else:
                movie_to_update = sorted_filtered_matches[int(user_choice) - 1][0]
                print(f"You can update the rating for '{movie_to_update}' ...")
                break

        while True:
            try:
                rating = input("\nEnter a new rating between 0 and 10 ('q' to cancel, 'c' to continue): ").strip()

                if rating.lower() == "q":
                    print("Action cancelled.")
                    return

                if rating.lower() == "c":
                    new_rating = movies[movie_to_update]["rating"]
                    break

                new_rating = float(rating.replace(",", "."))
                if not 0 <= new_rating <= 10:
                    print(f"Invalid rating! Please enter a number between 0 and 10.")
                    continue
                new_rating = str(new_rating)
                break

            except ValueError:
                print("Invalid rating! Please enter a number between 0 and 10.")

        while True:
            movies_notes = input("Enter movie notes if you like or 'q' to exit the update: ").strip()

            if movies_notes.lower() == "q":
                print("No movies notes added.")
                break

            if not movies_notes.strip():
                print("Please write something or 'q' if you wish to exit.")
                continue
            break

        self._data_storage.update_movie(movie_to_update, new_rating, movies_notes)
        print(f"Movie {movie_to_update} successfully updated!")


    def _command_movie_stats(self):
        """
        Display statistics for all movies,
        including average, median, best,
        and worst ratings.
        """
        movies = self._data_storage.list_movies()

        sorted_ratings = sorted(float(info["rating"]) for info in movies.values())

        average_rating = sum(sorted_ratings) / len(sorted_ratings)
        print(f"Average rating: {round(average_rating, 2)}")

        ratings_count = len(sorted_ratings)
        mid_index = ratings_count // 2

        if ratings_count % 2 == 0:
            median_rating = (sorted_ratings[mid_index - 1] + sorted_ratings[mid_index]) / 2
        else:
            median_rating = sorted_ratings[mid_index]

        print(f"Median rating: {round(median_rating, 2)}")

        highest_rating = max(float(info["rating"]) for info in movies.values())
        highest_rated_movies = [title for title, info in movies.items() if float(info["rating"]) == highest_rating]

        if len(highest_rated_movies) == 1:
            print(f"Highest rated movie: {highest_rated_movies[0]} (Rating: {highest_rating})")
        else:
            print(f"Highest rated movies: {', '.join(highest_rated_movies)} (Rating: {highest_rating})")

        lowest_rating = min(float(info["rating"]) for info in movies.values())
        lowest_rated_movies = [title for title, info in movies.items() if float(info["rating"]) == lowest_rating]

        if len(lowest_rated_movies) == 1:
            print(f"Lowest rated movie: {lowest_rated_movies[0]} (Rating: {lowest_rating})")
        else:
            print(f"Lowest rated movies: {'; '.join(lowest_rated_movies)} (Rating: {lowest_rating})")


    def _command_get_random_movie(self):
        """
        Suggest a random movie from the storage for the user to watch.
        """
        movies = self._data_storage.list_movies()

        database_tuple_ls = list(movies.items())
        random_selection = random.choice(database_tuple_ls)
        print(f"Your movie for tonight: {random_selection[0]}, it's rated {random_selection[1]['rating']}.")


    def _command_search_movie(self):
        """
        Search for movies based on a partial
        name using fuzzy string matching.
        """
        movies = self._data_storage.list_movies()

        while True:
            title = input("Enter part of the movie title (or 'q' to cancel): \n").casefold()

            if title.lower() == "q":
                print("Action cancelled.")
                return

            # check for empty string
            if not title.strip():
                print("Invalid input! Title cannot be empty.")
                continue

            # fuzzymatch module: using process.extract() to get best matches
            best_matches = process.extract(title, movies.keys(), limit=5)

            # manually filter matches based on score threshold
            filtered_matches = [(movie, score) for movie, score in best_matches if score >= 70]
            sorted_filtered_matches = sorted(filtered_matches, key=lambda item: item[1], reverse=True)

            if sorted_filtered_matches:
                for movie, score in sorted_filtered_matches:
                    print(f"{movie} ({movies[movie]['year']}): {movies[movie]['rating']}")
                break

            else:
                print(f"No matches found, try again ...")
                continue


    def _command_sort_movies_desc(self):
        """
        Sort and display all movies by their rating in descending order.
        """
        movies = self._data_storage.list_movies()

        sorted_movie_list = sorted(movies.items(), key=lambda item: float(item[1]["rating"]), reverse=True)
        for movie in sorted_movie_list:
            print(f"{movie[0]}: {movie[1]['rating']}")


    def _generate_website(self):
        """
        Generate a website displaying the movie database.
        """
        # Read the HTML template from a file
        with open("static/index_template.html", "r", encoding="utf-8") as handle:
            html_template = handle.read()

        movies = self._data_storage.list_movies()
        movie_items = []

        for title, info in movies.items():
            note = info.get("notes", "")
            imdb_id = info.get("imdb_id")
            imdb_url = f"https://www.imdb.com/title/{imdb_id}"
            movie_items.append(f"""
        <li>
            <div class="movie">
                <a href="{imdb_url}" target="_blank">
                    <img class="movie-poster" src="{info["poster"]}" title="{note}">
                </a>
                <div class="movie-title">{title}</div>
                <div class="movie-year">{info["year"]}</div>
                <div class="movie-rating">{info["rating"]}</div>
            </div>
        </li>""")

        movie_grid = "\n".join(movie_items)

        full_html = html_template.replace("__TEMPLATE_TITLE__", "I LOVE CINEMA")
        full_html = full_html.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

        with open("static/index.html", "w", encoding="utf-8") as handle:
            handle.write(full_html)

        print("Website was generated successfully.")


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
            user_input = input("Enter choice (0-9): ").strip()
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