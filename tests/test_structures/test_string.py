# -*- coding: utf-8 -*-
import time

from a3redis.structures import String
from ..base_redis_test_case import BaseRedisTestCase


class StringTestCase(BaseRedisTestCase):

    def test__set__get__success(self):
        # 附带测2个基类函数：exists, delete
        value = 'value'
        redis_string = String(main_key='test', rdb=self.rdb)
        redis_string.set(value)

        self.assertTrue(redis_string.exists())
        self.assertEqual(redis_string.get(), value)
        redis_string.delete()
        self.assertFalse(redis_string.exists())

    def test__increase__success(self):
        # 附带测1个基类函数：expire
        value = 166
        redis_string = String(main_key='test', rdb=self.rdb)
        redis_string.set(value)

        redis_string.increase(value)
        self.assertEqual(int(redis_string.get()), value * 2)

        redis_string.expire(1)
        self.assertTrue(redis_string.exists())
        time.sleep(1)
        self.assertFalse(redis_string.exists())

    def test__set_if_not_exists__success(self):
        value = 'value'
        redis_string = String(main_key='test', rdb=self.rdb)
        redis_string.delete()

        redis_string.set_if_not_exists(value)
        self.assertTrue(redis_string.exists())

        self.assertFalse(redis_string.set_if_not_exists(value + value))
        self.assertEqual(redis_string.get(), value)

    def test__main_key_format__success(self):
        redis_string = String(main_key='string:{key_name}', rdb=self.rdb, key_name='test')
        redis_string.increase()

        self.assertTrue(redis_string.exists())
