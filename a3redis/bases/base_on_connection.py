# -*- coding: utf-8 -*-
from abc import ABC
import redis

from .redis_client_factory import RedisClientFactory


class BaseOnConnection(ABC):
    rdb: redis.Redis = None

    def __init__(self, rdb: redis.Redis = None):
        self.rdb = rdb or self.rdb or RedisClientFactory.get_rdb()
