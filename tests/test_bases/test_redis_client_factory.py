# -*- coding: utf-8 -*-
import redis
from a3redis.bases import RedisClientFactory
from tests.base_redis_test_case import BaseRedisTestCase


class T(BaseRedisTestCase):

    def test__sentinel__success(self):
        master_rdb = RedisClientFactory.get_rdb('sentinel', readonly=False)
        key = 'key'
        value = 'value'
        master_rdb.set(key, value)
        self.assertEqual(master_rdb.get('key'), value)

        slave_rdb = RedisClientFactory.get_rdb('sentinel', readonly=True)
        self.assertEqual(slave_rdb.get('key'), value)
        with self.assertRaises(redis.exceptions.ReadOnlyError):
            slave_rdb.set(key, value)
