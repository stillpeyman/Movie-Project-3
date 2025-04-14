from movie_app import MovieApp
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv


if __name__ == "__main__":
    # Initialize storage objects, constructor in <__init__> knows the file path
    json_storage = StorageJson()
    csv_storage = StorageCsv()

    # Initialize the app with storage objects
    movie_app = MovieApp(json_storage, csv_storage)
    movie_app.run()