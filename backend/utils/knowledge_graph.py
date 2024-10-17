# backend/utils/knowledge_graph.py

import time
from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
import urllib.error

def query_wikidata(claim, max_retries=3, delay=1):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    # Escape { and } by doubling them
    query = """
    SELECT ?item ?itemLabel ?itemDescription WHERE {{
      ?item rdfs:label "{}"@en.
      OPTIONAL {{ ?item schema:description ?itemDescription. FILTER(LANG(?itemDescription) = "en") }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT 5
    """.format(claim)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    for attempt in range(max_retries):
        try:
            results = sparql.query().convert()
            return results
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print(f"HTTP Error: {e.code} - {e.reason}")
                break
        except Exception as e:
            print(f"Error querying Wikidata: {e}")
            break
    # Return empty results if all retries fail
    return {"results": {"bindings": []}}

def extract_texts_from_kg_results(results):
    texts = []
    bindings = results.get("results", {}).get("bindings", [])
    if not bindings:
        return texts
    for result in bindings:
        item_label = result["itemLabel"]["value"]
        item_description = result.get("itemDescription", {}).get("value", "")
        text = f"{item_label}: {item_description}"
        texts.append(text)
    return texts
