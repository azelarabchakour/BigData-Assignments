from neo4j import GraphDatabase
import requests

URI = "neo4j://127.0.0.1:7687"
AUTH = ("neo4j", "amnqU4LveHgvhCQ6FYQu")
BASE_URL = "https://swapi.info/api/"
ENDPOINTS = ["films", "people", "planets", "species", "vehicles", "starships"]

def fetch_all_data():
    """Fetches all JSON payloads from the 6 SWAPI endpoints."""
    db_data = {}
    for endpoint in ENDPOINTS:
        response = requests.get(f"{BASE_URL}{endpoint}")
        response.raise_for_status()
        # swapi.info returns the full list directly, no pagination needed
        db_data[endpoint] = response.json() 
    return db_data

def setup_constraints(driver):
    """Ensures idempotency by making the 'url' property unique for all nodes."""
    labels = ["Film", "Person", "Planet", "Species", "Vehicle", "Starship"]
    for label in labels:
        driver.execute_query(
            f"CREATE CONSTRAINT IF NOT EXISTS FOR (n:{label}) REQUIRE n.url IS UNIQUE",
            database_="swapi"
        )

def load_nodes(driver, db_data):
    """PASS 1: Creates nodes, maps all scalar fields, and casts numerics safely."""
    
    # 1. Films
    for film in db_data['films']:
        driver.execute_query("""
            MERGE (f:Film {url: $data.url})
            SET f.title = $data.title,
                f.episode_id = toInteger($data.episode_id),
                f.director = $data.director,
                f.producer = $data.producer,
                f.release_date = date($data.release_date),
                f.created = datetime($data.created),
                f.edited = datetime($data.edited)
            """, data=film, database_="swapi")
    
    # 2. People
    for person in db_data['people']:
        driver.execute_query("""
            MERGE (p:Person {url: $data.url})
            SET p.name = $data.name,
                p.hair_color = $data.hair_color,
                p.skin_color = $data.skin_color,
                p.eye_color = $data.eye_color,
                p.birth_year = $data.birth_year,
                p.gender = $data.gender,
                p.created = datetime($data.created),
                p.edited = datetime($data.edited),
                // Handle "unknown" values cleanly before converting to math types
                p.height = toInteger(CASE WHEN $data.height IN ['unknown', 'n/a'] THEN null ELSE $data.height END),
                p.mass = toFloat(CASE WHEN $data.mass IN ['unknown', 'n/a'] THEN null ELSE $data.mass END)
            """, data=person, database_="swapi")
        
    # 3. Planets
    for planet in db_data['planets']:
        driver.execute_query("""
            MERGE (p:Planet {url: $data.url})
            SET p.name = $data.name,
                p.climate = $data.climate,
                p.gravity = $data.gravity,
                p.terrain = $data.terrain,
                p.created = datetime($data.created),
                p.edited = datetime($data.edited),
                p.rotation_period = toInteger(CASE WHEN $data.rotation_period IN ['unknown', 'n/a'] THEN null ELSE $data.rotation_period END),
                p.orbital_period = toInteger(CASE WHEN $data.orbital_period IN ['unknown', 'n/a'] THEN null ELSE $data.orbital_period END),
                p.diameter = toInteger(CASE WHEN $data.diameter IN ['unknown', 'n/a'] THEN null ELSE $data.diameter END),
                p.surface_water = toInteger(CASE WHEN $data.surface_water IN ['unknown', 'n/a'] THEN null ELSE $data.surface_water END),
                p.population = toInteger(CASE WHEN $data.population IN ['unknown', 'n/a'] THEN null ELSE $data.population END)
            """, data=planet, database_="swapi")

    # 4. Species
    for species in db_data['species']:
        driver.execute_query("""
            MERGE (s:Species {url: $data.url})
            SET s.name = $data.name,
                s.classification = $data.classification,
                s.designation = $data.designation,
                s.skin_colors = $data.skin_colors,
                s.hair_colors = $data.hair_colors,
                s.eye_colors = $data.eye_colors,
                s.language = $data.language,
                s.created = datetime($data.created),
                s.edited = datetime($data.edited),
                s.average_height = toInteger(CASE WHEN $data.average_height IN ['unknown', 'n/a'] THEN null ELSE $data.average_height END),
                s.average_lifespan = toInteger(CASE WHEN $data.average_lifespan IN ['unknown', 'n/a'] THEN null ELSE $data.average_lifespan END)
            """, data=species, database_="swapi")

    # 5. Vehicles 
    for vehicle in db_data['vehicles']:
        driver.execute_query("""
            MERGE (v:Vehicle {url: $data.url})
            SET v.name = $data.name, 
                v.model = $data.model,
                v.manufacturer = $data.manufacturer,
                v.consumables = $data.consumables,
                v.vehicle_class = $data.vehicle_class,
                v.created = datetime($data.created),
                v.edited = datetime($data.edited),
                v.cost_in_credits = toInteger(CASE WHEN $data.cost_in_credits IN ['unknown', 'n/a'] THEN null ELSE $data.cost_in_credits END),
                v.length = toFloat(CASE WHEN $data.length IN ['unknown', 'n/a'] THEN null ELSE $data.length END),
                v.max_atmosphering_speed = toInteger(CASE WHEN $data.max_atmosphering_speed IN ['unknown', 'n/a'] THEN null ELSE $data.max_atmosphering_speed END),
                v.crew = $data.crew, // Left as string because SWAPI often formats this as a range e.g., "30-165"
                v.passengers = $data.passengers,
                v.cargo_capacity = toInteger(CASE WHEN $data.cargo_capacity IN ['unknown', 'n/a'] THEN null ELSE $data.cargo_capacity END)
            """, data=vehicle, database_="swapi")

    # 6. Starships
    for starship in db_data['starships']:
        driver.execute_query("""
            MERGE (s:Starship {url: $data.url})
            SET s.name = $data.name, 
                s.model = $data.model,
                s.manufacturer = $data.manufacturer,
                s.consumables = $data.consumables,
                s.starship_class = $data.starship_class,
                s.created = datetime($data.created),
                s.edited = datetime($data.edited),
                s.cost_in_credits = toInteger(CASE WHEN $data.cost_in_credits IN ['unknown', 'n/a'] THEN null ELSE $data.cost_in_credits END),
                s.length = toFloat(CASE WHEN $data.length IN ['unknown', 'n/a'] THEN null ELSE $data.length END),
                s.max_atmosphering_speed = $data.max_atmosphering_speed, // Left as string because SWAPI formats these weirdly like "1000km"
                s.crew = $data.crew,
                s.passengers = $data.passengers,
                s.cargo_capacity = toInteger(CASE WHEN $data.cargo_capacity IN ['unknown', 'n/a'] THEN null ELSE $data.cargo_capacity END),
                s.hyperdrive_rating = toFloat(CASE WHEN $data.hyperdrive_rating IN ['unknown', 'n/a'] THEN null ELSE $data.hyperdrive_rating END),
                s.MGLT = toInteger(CASE WHEN $data.MGLT IN ['unknown', 'n/a'] THEN null ELSE $data.MGLT END)
            """, data=starship, database_="swapi")
        
def load_relationships(driver, db_data):
    """PASS 2: Connects nodes. Only one side of a bidirectional API relationship is parsed to avoid redundancy."""
    
    # 1. FILM REFERENCES -> Connect all entities to the films they appear in
    for film in db_data['films']:
        film_url = film['url']
        
        for planet_url in film.get('planets', []):
            driver.execute_query("""
                MATCH (f:Film {url: $f_url}), (p:Planet {url: $p_url})
                MERGE (p)-[:APPEARS_IN]->(f)
            """, f_url=film_url, p_url=planet_url, database_="swapi")
            
        for char_url in film.get('characters', []):
            driver.execute_query("""
                MATCH (f:Film {url: $f_url}), (p:Person {url: $p_url})
                MERGE (p)-[:APPEARS_IN]->(f)
            """, f_url=film_url, p_url=char_url, database_="swapi")
            
        for starship_url in film.get('starships', []):
            driver.execute_query("""
                MATCH (f:Film {url: $f_url}), (s:Starship {url: $s_url})
                MERGE (s)-[:APPEARS_IN]->(f)
            """, f_url=film_url, s_url=starship_url, database_="swapi")
            
        for vehicle_url in film.get('vehicles', []):
            driver.execute_query("""
                MATCH (f:Film {url: $f_url}), (v:Vehicle {url: $v_url})
                MERGE (v)-[:APPEARS_IN]->(f)
            """, f_url=film_url, v_url=vehicle_url, database_="swapi")
            
        # FIXED: Added the missing Species -> Film relationship
        for species_url in film.get('species', []):
            driver.execute_query("""
                MATCH (f:Film {url: $f_url}), (s:Species {url: $s_url})
                MERGE (s)-[:APPEARS_IN]->(f)
            """, f_url=film_url, s_url=species_url, database_="swapi")

    # 2. PERSON REFERENCES -> Connect Homeworlds, Species, and Piloting
    # (We skip the 'films' array here because we already created the APPEARS_IN edge above)
    for person in db_data['people']:
        person_url = person['url']
        
        if person.get('homeworld'):
            driver.execute_query("""
                MATCH (p:Person {url: $p_url}), (pl:Planet {url: $pl_url})
                MERGE (p)-[:COMES_FROM]->(pl)
            """, p_url=person_url, pl_url=person['homeworld'], database_="swapi")
            
        for species_url in person.get('species', []):
            driver.execute_query("""
                MATCH (p:Person {url: $p_url}), (s:Species {url: $s_url})
                MERGE (p)-[:BELONGS_TO]->(s)
            """, p_url=person_url, s_url=species_url, database_="swapi")

        for vehicle_url in person.get('vehicles', []):
            driver.execute_query("""
                MATCH (p:Person {url: $p_url}), (v:Vehicle {url: $v_url})
                MERGE (p)-[:PILOTS]->(v)
            """, p_url=person_url, v_url=vehicle_url, database_="swapi")
            
        for starship_url in person.get('starships', []):
            driver.execute_query("""
                MATCH (p:Person {url: $p_url}), (s:Starship {url: $s_url})
                MERGE (p)-[:PILOTS]->(s)
            """, p_url=person_url, s_url=starship_url, database_="swapi")

    # 3. SPECIES REFERENCES -> Connect Homeworlds
    # (We skip 'people' and 'films' because they are handled in the loops above)
    for species in db_data['species']:
        if species.get('homeworld'):
            driver.execute_query("""
                MATCH (s:Species {url: $s_url}), (pl:Planet {url: $pl_url})
                MERGE (s)-[:COMES_FROM]->(pl)
            """, s_url=species['url'], pl_url=species['homeworld'], database_="swapi")

if __name__ == "__main__":
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        print("1. Fetching all SWAPI data...")
        swapi_data = fetch_all_data()

        print("2. Setting up uniqueness constraints...")
        setup_constraints(driver)
        
        print("3. PASS 1: Creating nodes and casting numeric properties...")
        load_nodes(driver, swapi_data)

        print("4. PASS 2: Mapping directed relationships...")
        load_relationships(driver, swapi_data)

        print("Import completely finished!")