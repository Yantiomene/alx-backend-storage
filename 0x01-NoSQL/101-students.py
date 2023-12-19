#!/usr/bin/env python3
"""Python function that returns all students sorted by average score:
Prototype: def top_students(mongo_collection):
mongo_collection will be the pymongo collection object
The top must be ordered
The average score must be part of each item returns with key = averageScore
"""


def top_students(mongo_collection):
    """List all student sorted by average score
    Args:
         mongo_collection: pymongo collection
    Return:
           list of student ordered
    """
    result = mongo_collection.aggregate([
        {"$unwind": "$topics"},
        {"$group": {
            "_id": "$_id",
            "averageScore": {
                "$avg": '$topics.score'
                        },
            "name": {"$first": "$name"}
                }
         },
        {"$sort": {"averageScore": -1}}
        ])
    return result
