# -*- coding: utf-8 -*-
import unittest
import redis
from a3redis.bases import RedisClientFactory, RedisMode
from a3redis.bases.redis_client_factory import DEFAULT_NAME

ALL_CONF = {
    # 还有一个默认的redis://127.0.0.1:6379/0，没有明写
    RedisMode.Standalone: {
        'mode': RedisMode.Standalone,
        'init': {
            'host': 'standalone-redis-master',
            'port': 6379,
            'db': 0,
            'password': RedisMode.Standalone,
            'decode_responses': True
        }
    },
    RedisMode.Sentinel: {
        'mode': RedisMode.Sentinel,
        'init': {
            'sentinels': [
                ('sentinel-redis-node-0.sentinel-redis-headless', 26379),
                ('sentinel-redis-node-1.sentinel-redis-headless', 26379),
                ('sentinel-redis-node-2.sentinel-redis-headless', 26379)
            ],
            'sentinel_kwargs': {
                'password': RedisMode.Sentinel
            },
            'password': RedisMode.Sentinel,
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
            'port': 6379,
            'password': RedisMode.Cluster,
            'decode_responses': True
        }
    }

}


class BaseRedisTestCase(unittest.TestCase):
    rdb: redis.Redis = None
    redis_name = DEFAULT_NAME

    @classmethod
    def setUpClass(cls):
        RedisClientFactory.init_redis_clients(ALL_CONF)

    def setUp(self) -> None:
        self.rdb = RedisClientFactory.get_rdb(self.redis_name)

    def tearDown(self) -> None:
        if self.redis_name != RedisMode.Cluster:
            self.rdb.flushdb()
