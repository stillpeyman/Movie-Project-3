import json
import csv
import os
from dotenv import load_dotenv
import requests


load_dotenv()
API_KEY = os.getenv("API_KEY")
HOST = "www.omdbapi.com"


def get_movie_data(title):
    """
    Fetches movie data from OMDb and saves it to 'response.json' and 'response.csv'.

    Returns the movie data as a dictionary.

    Raises:
        ValueError: If movie is not found or API returns an error.
    """
    api_url = f"http://{HOST}/?apikey={API_KEY}&t={title}"

    # simple connection test
    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            movie_data = response.json()

            if movie_data.get("Response") == "False":
                # Get value of "Error" key from response.json, else return "Unknown Error!"
                raise ValueError(movie_data.get("Error", "Unknown Error"))

            with open("response.json", "w", encoding="utf-8") as handle:
                json.dump(movie_data, handle, indent=4)

            # with open("response.csv", "w", encoding="utf-8", newline="") as handle:
            #     fieldnames = movie_data.keys()
            #
            #     writer = csv.DictWriter(handle, fieldnames=fieldnames)
            #     writer.writeheader()
            #     writer.writerow(movie_data)

            return movie_data

        else:
            print(f"Error occurred: {response.status_code}")

    except requests.exceptions.ConnectionError as e:
        print("ConnectionError: ", e)

