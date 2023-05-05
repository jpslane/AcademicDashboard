import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import scholar

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='test_root',
    database='academicworld'
)
engine = create_engine('mysql+mysqlconnector://root:test_root@localhost:3306/academicworld')


def get_keywords():
    with engine.connect() as con:
        return pd.read_sql("SELECT DISTINCT name FROM keyword", con=con)


def get_years():
    with engine.connect() as con:
        return pd.read_sql("SELECT DISTINCT year FROM publication ORDER BY year DESC", con=con)


def get_uni():
    with engine.connect() as con:
        return pd.read_sql("SELECT DISTINCT name FROM university ORDER BY name", con=con)


def get_faculty():
    with engine.connect() as con:
        return pd.read_sql("SELECT DISTINCT name FROM faculty ORDER BY name", con=con)


def get_university():
    with engine.connect() as con:
        return pd.read_sql("SELECT COUNT(*) FROM university", con=con)


def read_sql(query):
    with engine.connect() as con:
        pd.read_sql(query, con=con)


def find_faculty_member(keyword):
    cursor = db.cursor(prepared=True)  # prepared statement

    query1 = """
        SELECT faculty.name as Faculty, university.name as University, COUNT(publication.id) AS "Publication Count"
        FROM faculty, faculty_publication, publication_keyword, university, publication, keyword
        WHERE faculty.id = faculty_publication.faculty_id
        AND faculty_publication.publication_id = publication.id
        AND publication.id = publication_keyword.publication_id
        AND keyword.id = publication_keyword.keyword_id
        AND faculty.university_id = university.id
        AND keyword.name = %s
        GROUP BY faculty.name, university.name
        HAVING count(publication.id) > 1
        ORDER BY count(publication.id) DESC
        LIMIT 20;
    """
    query2 = """
        SELECT faculty.name as Faculty, faculty_keyword.score as Score
        FROM faculty
        JOIN faculty_keyword ON faculty.id = faculty_keyword.faculty_id
        JOIN keyword ON faculty_keyword.keyword_id = keyword.id
        WHERE keyword.name = %s
        GROUP BY faculty.name, faculty_keyword.score
        ORDER BY faculty_keyword.score DESC;
    """
    keyword = (keyword,)
    cursor.execute(query1, keyword)
    result = cursor.fetchall()
    df1 = pd.DataFrame(result, columns=['Faculty', 'University', f'Publication Count for Publications with Keyword'])
    cursor.execute(query2, keyword)
    result = cursor.fetchall()
    df2 = pd.DataFrame(result, columns=['Faculty', 'Faculty Score in Relation to Keyword'])
    cursor.close()
    df = pd.merge(df1, df2, on='Faculty', how='left')
    df['Google Scholar'] = df.apply(lambda row: scholar.get_scholar(row['Faculty']), axis=1)
    return df


def return_db():
    return db
