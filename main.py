from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv


if __name__ == "__main__":
    storage_type = input("Choose storage type (json or csv): ").strip().lower()

    if storage_type == "json":
        storage = StorageJson('movie_database.json')
    elif storage_type == "csv":
        storage = StorageCsv('movie_database.csv')
    else:
        print("Invalid choice! Defaulting to JSON storage.")
        storage = StorageJson('movie_database.json')

    movie_app = MovieApp(storage)
    movie_app.run()