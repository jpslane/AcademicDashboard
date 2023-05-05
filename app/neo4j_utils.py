import neo4j as n4
import pandas as pd
import get_coordinates

uri = "bolt://localhost:7687"
driver = n4.GraphDatabase.driver(uri, auth=("neo4j", "cs411"))

default = ""


def run_query(query):
    with driver.session(database='academicworld') as session:
        result = session.run(query)
        return pd.DataFrame(result.data())


def return_faculty_count(keyword):
    query1 = f"MATCH (f:FACULTY)-[:PUBLISH]->(p:PUBLICATION)-[:LABEL_BY]->(k:KEYWORD) WHERE k.name = {keyword} " \
             f"RETURN " \
             f"p.year AS year, COUNT(DISTINCT f.id) AS faculty_count ORDER BY year"
    query2 = f"""MATCH (p:PUBLICATION)-[:LABEL_BY]->(k:KEYWORD) 
                WHERE k.name = {keyword}
                RETURN p.year as year, COUNT(DISTINCT p.id) AS publication_count ORDER BY year"""

    with driver.session(database='academicworld') as session:
        result1 = session.run(query1)
        result2 = session.run(query2)
        return pd.DataFrame(result1.data()), pd.DataFrame(result2.data())


def return_university_interest(keyword):
    query = f"""MATCH (inst:INSTITUTE)-[:AFFILIATION_WITH]-(f:FACULTY)-[:PUBLISH]->(p:PUBLICATION)-[:LABEL_BY]->(
    k:KEYWORD) WHERE k.name = {keyword} RETURN inst.name as university, COUNT(p) as count ORDER BY COUNT(p) DESC LIMIT 20"""

    with driver.session(database='academicworld') as session:
        result = session.run(query)
        df = pd.DataFrame(result, columns=['university', 'count'])
        df[['latitude', 'longitude']] = df['university'].apply(get_coordinates.get_coordinate).apply(pd.Series)

        return df