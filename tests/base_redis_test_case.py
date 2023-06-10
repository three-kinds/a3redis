# -*- coding: utf-8 -*-
import unittest
import redis
from a3redis.bases import RedisClientFactory, RedisMode


ALL_CONF = {
    RedisMode.Standalone: {
        'mode': RedisMode.Standalone,
        'init': {
            'host': 'redis-node-0.redis-headless',
            'port': 6379,
            'db': 0,
            'password': "123456",
            'decode_responses': True
        }
    },
    RedisMode.Sentinel: {
        'mode': RedisMode.Sentinel,
        'init': {
            'sentinels': [
                ('redis-node-0.redis-headless', 26379),
                ('redis-node-1.redis-headless', 26379),
                ('redis-node-2.redis-headless', 26379)
            ],
            'sentinel_kwargs': {
                'password': '123456'
            },
            'password': '123456',
            'db': 1,
            'decode_responses': True,
        },
        'runtime': {
            'service_name': 'my-master'
        }
    },
    RedisMode.Cluster: {
        'mode': RedisMode.Cluster,
        'init': {
            'host': "cluster-redis-cluster",
            'port': "6379",
            'password': "123456",
        }
    }

}


class BaseRedisTestCase(unittest.TestCase):
    rdb: redis.Redis = None
    redis_name = 'default'

    def setUpClass(cls):
        RedisClientFactory.init_redis_clients(ALL_CONF)

    def setUp(self) -> None:
        self.rdb = RedisClientFactory.get_rdb(self.redis_name)

    def tearDown(self) -> None:
        self.rdb.flushdb()
