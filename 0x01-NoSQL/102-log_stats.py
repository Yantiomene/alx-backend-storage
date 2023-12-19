#!/usr/bin/env python3
"""Python script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


def top_ip(mongo_collection):
    """Get the top 10 most present IP
    Args:
         mongo_collection: pymongo collection
    Return:
           list of top 10 IPS
    """
    result = mongo_collection.aggregate([
        {"$group": {
            "_id": "$ip",
            "count": {
                "$sum": 1
                }
            }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10}
        ])

    return result


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_col = client.logs.nginx

    print("{} logs".format(nginx_col.count_documents({})))
    print("{}".format(nginx_col.find()[0]))
    print("Methods:")
    method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for meth in method:
        print("\tmethod {}: {}".format(
            meth,
            nginx_col.count_documents({'method': meth})))

    print("{} status check".format(
        nginx_col.count_documents({'method': 'GET', 'path': '/status'})))
    print("IPs:")
    top_ips = top_ip(nginx_col)
    for ip in top_ips:
        print("\t{}: {}".format(ip.get('_id'), ip.get('count')))
