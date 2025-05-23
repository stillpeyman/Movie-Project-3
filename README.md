
# Movie Database App

This project is a movie database application that allows users to manage and display a collection of movies. The app stores movie data in both JSON and CSV formats, integrates with the OMDb API to fetch movie information, and generates a simple website to display the movies with their posters, release years, and ratings.

## Features

- Add, update, delete, and list movies.
- Fetch movie information using the OMDb API.
- Display a list of movies in a grid layout with posters, titles, years, and ratings.
- Generate a static HTML website displaying the movie collection.

## Project Structure

```
movie_app/
├── api/
│   ├── omdb_api.py          # OMDb API integration.
├── app/
│   ├── main.py              # Main app entry point.
│   ├── movie_app.py         # Movie app logic and website generation.
├── data/
│   ├── movies.json          # Movie data in JSON format.
│   ├── movies.csv           # Movie data in CSV format.
├── static/
│   ├── index.html           # Generated website for displaying movies.
│   ├── style.css            # CSS styles for the website.
├── storage/
│   ├── istorage.py          # Storage interface.
│   ├── storage_json.py      # JSON-based storage implementation.
│   ├── storage_csv.py       # CSV-based storage implementation.
├── requirements.txt         # Python dependencies.
└── README.md                # Project documentation.
```

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/movie-database-app.git
   ```

2. Navigate to the project directory:

   ```
   cd movie-database-app
   ```

3. Create a virtual environment:

   ```
   python3 -m venv venv
   ```

4. Activate the virtual environment:

   - For macOS/Linux:
     ```
     source venv/bin/activate
     ```
   - For Windows:
     ```
     venv\Scripts\activate
     ```

5. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the App

To run the app and generate the website, execute the following command:

```
python3 -m app.main <filename.json|filename.csv>
```

- Replace `<filename.json|filename.csv>` with the path to your movie data file (either `movies.json` or `movies.csv`).
- The app will process the movie data and generate a `static/index.html` file with the list of movies, including posters, titles, years, and ratings.

### Adding or Updating Movies

Movies can be added or updated in the app by modifying the `movies.json` or `movies.csv` file or using the provided methods in `movie_app.py`.

### Generating the Website

The website is generated by calling the `_generate_website()` method in `movie_app.py`, which uses the movie data to create the HTML content.

## Dependencies

The project requires the following Python libraries:

- **fuzzywuzzy==0.18.0**: For fuzzy string matching.
- **Levenshtein==0.27.1**: For faster string matching algorithms.
- **python-dotenv==1.1.0**: To load environment variables from `.env` files.
- **python-Levenshtein==0.27.1**: Optimized Levenshtein distance calculations.
- **requests==2.32.0**: For making HTTP requests to the OMDb API.

You can install these dependencies with:

```
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Developed by Peyman Farahani – SDE Trainee and film nerd.
