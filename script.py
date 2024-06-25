import json
from SPARQLWrapper import SPARQLWrapper, JSON

ENDPOINT_URL = "https://query.wikidata.org/sparql"

def start_sparql(endpoint: str) -> dict:
    """Start SPARQL connection with Wikidata and return results."""
    
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery("""
        SELECT ?film ?filmLabel ?abstract ?releaseDate ?directorLabel ?ageRating ?poster ?rating ?trailer ?genreLabel ?runtime
        WHERE {
          ?film wdt:P31 wd:Q11424.  # instance of film
          ?film wdt:P1476 ?filmLabel.  # title
          OPTIONAL { ?film schema:description ?abstract. FILTER(LANG(?abstract) = "en") }
          OPTIONAL { ?film wdt:P577 ?releaseDate. }
          OPTIONAL { ?film wdt:P57 ?director. }
          OPTIONAL { ?film wdt:P5646 ?ageRating. }
          OPTIONAL { ?film wdt:P154 ?poster. }
          OPTIONAL { ?film wdt:P444 ?rating. }
          OPTIONAL { ?film wdt:P1651 ?trailer. }
          OPTIONAL { ?film wdt:P136 ?genre. }
          OPTIONAL { ?film wdt:P2047 ?runtime. }
          FILTER(?releaseDate >= "2005-01-01T00:00:00Z"^^xsd:dateTime)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        }
        LIMIT 100
    """)
    sparql.setReturnFormat(JSON)
    
    results = sparql.query().convert()
    
    return results


def get_movies(results: dict) -> list:
    """Get movies from SPARQL results."""

    movies = []
    for result in results["results"]["bindings"]:
        movie = {
            "Film": result["film"]["value"],
            "Title": result["filmLabel"]["value"],
            "Plot": result.get("abstract", {}).get("value", "N/A"),
            "Released": result.get("releaseDate", {}).get("value", "N/A"),
            "Director": result.get("directorLabel", {}).get("value", "N/A"),
            "Rated": result.get("ageRating", {}).get("value", "N/A"),
            "Poster": result.get("poster", {}).get("value", "N/A"),
            "Ratings": result.get("rating", {}).get("value", "N/A"),
            "Trailer": result.get("trailer", {}).get("value", "N/A"),
            "Genre": result.get("genreLabel", {}).get("value", "N/A"),
            "Runtime": result.get("runtime", {}).get("value", "N/A")
        }
        movies.append(movie)        
    return movies


def save_json(movies: list):
    """Save data in json file."""
    
    with open('movies.json', 'w') as json_file:
        json.dump(movies, json_file, indent=4)


if __name__ == "__main__":
    results = start_sparql(ENDPOINT_URL)
    movies = get_movies(results)
    save_json(movies)
    print("Data saved in movies.json")