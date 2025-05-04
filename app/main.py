"""
Main entry point for the Movie App.

This script takes a .json or .csv filename as a command-line argument,
determines the file type, initializes the appropriate storage class,
and launches the MovieApp.

Usage:
    python3 -m app.main <filename.json|filename.csv>

Example:
    python3 -m app.main movies.json
"""

import os.path
import sys
from app.movie_app import MovieApp
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv
import argparse


# Add parent directory to sys.path (list of directories Python searches when trying to import modules)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="A Movie App for managing movie data stored in .json or .csv files.")
    parser.add_argument("filename", help="Path to the .json or .csv file where movie data is stored."
         "Use .json for structured data or .csv for spreadsheet-style data.")

    # Parse arguments
    args = parser.parse_args()

    filename = args.filename.lower()
    # Split filename into 2 parts, <name> and <ext> (extension)
    name, ext = os.path.splitext(filename)

    if ext == ".json":
        # Initialize storage objects, pass <filename> to <__init__>, create file path
        storage = StorageJson(filename)

    elif ext == ".csv":
        storage = StorageCsv(filename)

    else:
        print("Unsupported file type. Please use a .json or .csv file.")

    # Initialize the app with storage objects
    movie_app = MovieApp(storage)
    movie_app.run()
