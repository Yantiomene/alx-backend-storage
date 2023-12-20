#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
from typing import Union, Callable, Optional
import uuid
from functools import wraps


def replay(method: Callable) -> None:
    """Display the history of calls of a particular function"""

    r = redis.Redis()
    name = method.__qualname__
    count = r.get(name)
    try:
        count = int(count.decode("utf-8"))
    except Exception:
        count = 0

    print("{} was called {} times:".format(name, count))
    inputs = r.lrange("{}:inputs".format(name), 0, -1)
    outputs = r.lrange("{}:outputs".format(name), 0, -1)

    for inp, out in zip(inputs, outputs):
        try:
            inp = inp.decode("utf-8")
        except Exception:
            inp = ""

        try:
            out = out.decode("utf-8")
        except Exception:
            out = ""

        print("{}(*{}) -> {}".format(name, inp, out))


def call_history(method: Callable) -> Callable:
    """Decorator to store hsitory of inputs and outputs"""

    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for the decorator"""
        inputs = str(args)
        self._redis.rpush(input_key, inputs)
        outputs = str(method(self, *args, **kwargs))
        self._redis.rpush(output_key, outputs)

        return outputs

    return wrapper


def count_calls(method: Callable) -> Callable:
    """decorator use to count instances"""

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function for the decorator"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """Store an instance of the Redis client and flush the instance"""

    def __init__(self):
        """Store an instance of the redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generate a random key, store the input data in Redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Convert the data back to the desire format"""

        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Parametrize Cache.get with the correct conversion function"""

        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """Parametrize Cache.get with the correct conversion function"""

        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
