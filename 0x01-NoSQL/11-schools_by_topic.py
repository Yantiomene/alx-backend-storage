#!/usr/bin/env python3
"""returns the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """Lists all the schoool having a specific topic
    Args:
         mongo_collection: pymongo collection,
         topic: topic searched
    Return:
           List of school
    """
    return mongo_collection.find({"topics": topic})
