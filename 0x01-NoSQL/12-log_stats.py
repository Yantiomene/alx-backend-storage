#!/usr/bin/env python3
"""Python script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_col = client.logs.nginx

    print("{} logs".format(nginx_col.count_documents({})))
    print("Methods:")
    method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for meth in method:
        print("\tmethod {}: {}".format(
            meth,
            nginx_col.count_documents({'method': meth})))

    print("{} status check".format(
        nginx_col.count_documents({'method': 'GET', 'path': '/status'})))
