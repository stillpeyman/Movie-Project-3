from fuzzywuzzy import process


def command_delete_movie(database):
    """
    Prompt user to enter a movie title
    to delete from storage.
    """
    movies = database

    while True:
        user_input = input("Enter part of the movie title (or 'q' to cancel): ").casefold()

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
        print(sorted_filtered_matches)

        if sorted_filtered_matches:
            for i in range(len(sorted_filtered_matches)):
                    print(f"{i + 1}. {sorted_filtered_matches[i][0]}")
            break

        else:
            print(f"No matches found, try again ...")
            continue

    while True:
        user_choice = input("\nChoose the movie to delete by entering the number (or 'q' to cancel): ").strip()

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

    return movie_to_delete


data = {
    "Lawrence of Arabia": {
        "year": "1962",
        "rating": "8.3",
        "poster": "https://m.media-amazon.com/images/M/MV5BYjY0YTQ1OTAtYjEyNy00NTQ4LThlMTQtM2QwYTVhYWFhNjU5XkEyXkFqcGc@._V1_SX300.jpg"
    },
    "Anora": {
        "year": "2024",
        "rating": "9.5",
        "poster": "https://m.media-amazon.com/images/M/MV5BYThiN2M0NTItODRmNC00NDhlLWFiYTgtMWM2YTEyYzI3ZTY1XkEyXkFqcGc@._V1_SX300.jpg"
    },
    "Interstellar": {
        "year": "2014",
        "rating": "8.7",
        "poster": "https://m.media-amazon.com/images/M/MV5BYzdjMDAxZGItMjI2My00ODA1LTlkNzItOWFjMDU5ZDJlYWY3XkEyXkFqcGc@._V1_SX300.jpg"
    },
    "The Shining": {
        "year": "1980",
        "rating": "8.4",
        "poster": "https://m.media-amazon.com/images/M/MV5BNmM5ZThhY2ItOGRjOS00NzZiLWEwYTItNDgyMjFkOTgxMmRiXkEyXkFqcGc@._V1_SX300.jpg"
    },
    "The Godfather": {
        "year": "1972",
        "rating": "9.2",
        "poster": "https://m.media-amazon.com/images/M/MV5BNGEwYjgwOGQtYjg5ZS00Njc1LTk2ZGEtM2QwZWQ2NjdhZTE5XkEyXkFqcGc@._V1_SX300.jpg"
    },
    "The Godfather Part II": {
        "year": "1974",
        "rating": "9.0",
        "poster": "https://m.media-amazon.com/images/M/MV5BMDIxMzBlZDktZjMxNy00ZGI4LTgxNDEtYWRlNzRjMjJmOGQ1XkEyXkFqcGc@._V1_SX300.jpg"
    },
    "Apocalypse Now": {
        "year": "1979",
        "rating": "8.4",
        "poster": "https://m.media-amazon.com/images/M/MV5BZDhiMTljYjYtODc1Yy00MmEwLTg2OTYtYmE1YTRmNDE4MmEwXkEyXkFqcGc@._V1_SX300.jpg"
    },
    "2001: A Space Odyssey": {
        "year": "1968",
        "rating": "8.3",
        "poster": "https://m.media-amazon.com/images/M/MV5BNjU0NDFkMTQtZWY5OS00MmZhLTg3Y2QtZmJhMzMzMWYyYjc2XkEyXkFqcGc@._V1_SX300.jpg"
    },
    "There Will Be Blood": {
        "year": "2007",
        "rating": "8.2",
        "poster": "https://m.media-amazon.com/images/M/MV5BMjAxODQ4MDU5NV5BMl5BanBnXkFtZTcwMDU4MjU1MQ@@._V1_SX300.jpg"
    },
    "The Brutalist": {
        "year": "2024",
        "rating": "7.5",
        "poster": "https://m.media-amazon.com/images/M/MV5BM2U0MWRjZTMtMDVhNC00MzY4LTgwOTktZGQ2MDdiYTI4OWMxXkEyXkFqcGc@._V1_SX300.jpg"
    }
}

command_delete_movie(data)


# storage = StorageJson('movie_database.json')
# print(storage.list_movies())
# print()
# storage.add_movie("Mufasa", 2024, 4.5, "poster")
# print(storage.list_movies())
# print()
# storage.delete_movie("Mufasa")
# print(storage.list_movies())
# print()
# storage.delete_movie("Anora", 9.9)
# print(storage.list_movies())
# print()
# print(list(storage.list_movies().items()))

# import json
# import csv
#
# with open("movie_database.json", "r", encoding="utf-8") as handle:
#     movies = json.load(handle)
#
# rows = []
#
# for title, info in movies.items():
#     row = {
#         "title": title,
#         "year": info["year"],
#         "rating": info["rating"]
#     }
#     rows.append(row)
#
# with open("movie_database.csv", "w", encoding="utf-8") as handle:
#     fieldnames = ["title", "year", "rating", "poster"]
#     writer = csv.DictWriter(handle, fieldnames=fieldnames)
#
#     writer.writeheader()
#     writer.writerows(rows)

# """CONVERT MOVIE_DATABASE JSON TO CSV"""
# import csv
# import json
#
# with open("movie_database.json", "r") as handle:
#     movies = json.load(handle)
#
# print(movies)
#
# with open("movie_database.csv", "w") as handle:
#     fieldnames = ["title", "year", "rating", "poster"]
#     writer = csv.DictWriter(handle, fieldnames=fieldnames)
#     writer.writeheader()
#
#     rows = []
#     for title, info in movies.items():
#         row = {
#             "title": title,
#             "year": info["year"],
#             "rating": info["rating"],
#             "poster": info["poster"]
#         }
#         rows.append(row)
#
#     writer.writerows(rows)

