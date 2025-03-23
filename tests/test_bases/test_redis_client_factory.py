# -*- coding: utf-8 -*-
import redis
import random
from unittest import mock
from a3redis.bases import RedisClientFactory, RedisMode
from tests.base_redis_test_case import BaseRedisTestCase


class T(BaseRedisTestCase):
    def test__sentinel__success(self):
        master_rdb = RedisClientFactory.get_rdb(RedisMode.Sentinel, readonly=False)
        key = "key"
        value = "value"
        master_rdb.set(key, value)
        self.assertEqual(master_rdb.get("key"), value)

        slave_rdb = RedisClientFactory.get_rdb(RedisMode.Sentinel, readonly=True)
        self.assertEqual(slave_rdb.get("key"), value)
        with self.assertRaises(redis.exceptions.ReadOnlyError):
            slave_rdb.set(key, value)

    def test__sentinel__flush(self):
        p = mock.patch.object(RedisClientFactory, "is_valid_rdb", return_value=False)
        p.start()
        self.addCleanup(p.stop)
        key = "key"
        value = str(random.randint(10000, 999999))

        master_rdb = RedisClientFactory.get_rdb(RedisMode.Sentinel)
        master_rdb.set(key, value)
        slave_rdb = RedisClientFactory.get_rdb(RedisMode.Sentinel, readonly=True)
        self.assertEqual(slave_rdb.get(key), value)

    def test__cluster__success(self):
        rdb = RedisClientFactory.get_rdb(RedisMode.Cluster)
        key = "key"
        value = str(random.randint(10000, 999999))
        rdb.set(key, value)
        self.assertEqual(rdb.get(key), value)

        self.assertEqual(rdb.exists(key), True)
        rdb.delete(key)
        self.assertEqual(rdb.exists(key), False)

    def test__is_valid_rdb(self):
        self.assertTrue(RedisClientFactory.is_valid_rdb(self.rdb))

        p = mock.patch.object(redis.Redis, "ping", mock.Mock(side_effect=redis.RedisError("Mock Error")))
        p.start()
        self.addCleanup(p.stop)

        self.assertFalse(RedisClientFactory.is_valid_rdb(self.rdb))
