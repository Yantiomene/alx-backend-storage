#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
import typing
import uuid


class Cache:
    """Store an instance of the Redis client and flush the instance"""

    def __init__(self):
        """Store an instance of the redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: typing.Union[str, bytes, int, float]) -> str:
        """Generate a random key, store the input data in Redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key
