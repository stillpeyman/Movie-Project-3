# from storage_json import StorageJson
#
# storage = StorageJson('movie_database.json')
# print(storage.list_movies())
# print()
# storage.add_movie("Mufasa", 2024, 4.5, "poster")
# print(storage.list_movies())
# print()
# storage.delete_movie("Mufasa")
# print(storage.list_movies())
# print()
# storage.update_movie("Anora", 9.9)
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

