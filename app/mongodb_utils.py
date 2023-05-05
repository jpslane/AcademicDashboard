import pymongo
import pandas as pd

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['academicworld']


def most_popular_keywords_in_year(year):
    collection = db['publications']
    collection.create_index('keywords')
    result = collection.aggregate([
        {"$match": {"year": year}},
        {"$unwind": "$keywords"},
        {"$group": {"_id": "$keywords.name", "count": {"$sum": 1}, "total": {"$sum": "$keywords.score"}}},
        {"$sort": {"total": -1}},
        {"$limit": 100}
    ])

    return pd.DataFrame(list(result))

