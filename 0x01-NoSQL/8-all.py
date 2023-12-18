#!/usr/bin/env python3
"""Python function to list all documents in a collection"""


def list_all(mongo_collection):
    """Lists all documents in a collection
    Args:
         mongo_collection: pymongo collection
    Return:
           List of document or empty list
    """
    list_doc = list(mongo_collection.find())
    return list_doc

    
