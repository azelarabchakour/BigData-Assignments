from neo4j import GraphDatabase
import requests

# URI = "neo4j://127.0.0.1:7687"
# AUTH = ("neo4j", "amnqU4LveHgvhCQ6FYQu")

# with GraphDatabase.driver(URI, auth=AUTH) as driver:
#     driver.verify_connectivity()

#     records, summary, keys = driver.execute_query("""
#     MATCH (p1:Product)<-[:CONTAINS]-(o:Order)-[:CONTAINS]->(p2:Product)
#     WHERE p1.product_id < p2.product_id //To prevent duplicates
#     RETURN p1.product_name, p2.product_name, count(o) AS nbrTimeTogether
#     ORDER BY nbrTimeTogether DESC
#     """,
#     database_="e-commerce",
# )

#     # Loop through results and do something with them
#     for record in records:
#         print(record.data())  # obtain record as dict

#     # Summary information
#     print("The query `{query}` returned {records_count} records in {time} ms.".format(
#         query=summary.query, records_count=len(records),
#         time=summary.result_available_after
#     ))



def fetch_data():
    # 1. Define the API endpoint URL (using a sample public API)
    url = "https://swapi.info/api/films/1"

    try:
        # 2. Make a GET request to the API
        response = requests.get(url)
        
        # 3. Raise an exception if the request failed (e.g., 404 or 500 error)
        response.raise_for_status()
        
        # 4. Parse the JSON response into a Python dictionary
        data = response.json()
        
        # 5. Display the data
        print("--- API Response ---")
        print(f"User ID: {data.get('title')}")
        print(f"Title: {data.get('episode_id')}")
        print(f"Completed: {data.get('opening_crawl')}")
        
        print("\n--- Full Raw Data ---")
        print(data)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_data()
