# -*- coding: utf-8 -*-
from a3redis.structures import HyperLogLog
from ..base_redis_test_case import BaseRedisTestCase


class HyperLogLogTestCase(BaseRedisTestCase):

    def test__add__success(self):
        hll = HyperLogLog(main_key='test_hyper_log_log', rdb=self.rdb)
        self.assertEqual(hll.add('1'), 1)
        self.assertEqual(hll.add('1'), 0)
        self.assertEqual(hll.add(['1', '2', '3', '4']), 1)

    def test__get_length__success(self):
        hll = HyperLogLog(main_key='test_hyper_log_log', rdb=self.rdb)
        hll.add(['1', '2', '3', '4'])
        self.assertEqual(hll.get_length(), 4)
