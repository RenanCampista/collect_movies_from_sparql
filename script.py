import json
from SPARQLWrapper import SPARQLWrapper, JSON

ENDPOINT_URL = "https://dbpedia.org/sparql"

def start_sparql(endpoint: str) -> dict:
    """Start SPARQL connection with Wikidata and return results."""
    
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery("""
        SELECT ?film ?title ?abstract ?releaseDate ?director ?ageRating ?poster ?rating ?trailer ?genre ?runtime
        WHERE {
            ?film a dbo:Film .
            ?film rdfs:label ?title .
            OPTIONAL { ?film dbo:abstract ?abstract . }
            OPTIONAL { ?film dbo:releaseDate ?releaseDate . }
            OPTIONAL { ?film dbo:director ?director . }
            OPTIONAL { ?film dbo:ageRating ?ageRating . }
            OPTIONAL { ?film dbo:thumbnail ?poster . }
            OPTIONAL { ?film dbo:rating ?rating . }
            OPTIONAL { ?film dbo:trailer ?trailer . }
            OPTIONAL { ?film dbo:genre ?genre . }
            OPTIONAL { ?film dbo:runtime ?runtime . }
            FILTER (lang(?title) = 'en') .
            FILTER (lang(?abstract) = 'en') .
            FILTER (?releaseDate >= "2005-01-01"^^xsd:date)
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
            "Title": result["title"]["value"],
            "Plot": result.get("abstract", {}).get("value", "N/A"),
            "Released": result.get("releaseDate", {}).get("value", "N/A"),
            "Director": result.get("director", {}).get("value", "N/A"),
            "Rated": result.get("ageRating", {}).get("value", "N/A"),
            "Poster": result.get("poster", {}).get("value", "N/A"),
            "Ratings": result.get("rating", {}).get("value", "N/A"),
            "Trailer": result.get("trailer", {}).get("value", "N/A"),
            "Genre": result.get("genre", {}).get("value", "N/A"),
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