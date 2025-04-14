from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv


if __name__ == "__main__":
    json_storage = StorageJson('movie_database.json')
    csv_storage = StorageCsv('movie_database.csv')

    movie_app = MovieApp(json_storage, csv_storage)
    movie_app.run()