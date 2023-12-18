#!/usr/bin/env python3
"""Python function that changes all topics of a school document based on name"""


def update_topics(mongo_collection, name, topics):
    """Changes all topics of a school document
    Args:
         mongo_collection: pymongo collection,
         name: school name to update,
         topics: list of topics approached in the school
    Return:
          Nothing
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {
            "topics": topics
            }
         })
    
