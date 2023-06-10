# -*- coding: utf-8 -*-
from a3redis.structures import Hash
from ..base_redis_test_case import BaseRedisTestCase


class HashTestCase(BaseRedisTestCase):

    def test__set_get__success(self):
        a_hash = Hash(main_key='a_hash', rdb=self.rdb)
        a_hash.set_member('a', '1')
        a_hash['b'] = '2'
        a_hash.set_multi_members({
            'c': '3',
            'd': '4'
        })

        self.assertEqual(a_hash.get_length(), 4)
        self.assertEqual(a_hash.get_all_keys(), ['a', 'b', 'c', 'd'])
        self.assertEqual(a_hash.get_all_members(), {'a': '1', 'b': '2', 'c': '3', 'd': '4'})

        self.assertEqual(a_hash['a'], '1')
        self.assertEqual(a_hash.get_member_by_key('b'), '2')

        self.assertEqual(a_hash.get_length(), 4)
        a_hash.set_member_must_new('a', 'a')
        self.assertEqual(a_hash.get_length(), 4)
        a_hash.set_member_must_new('e', '5')
        self.assertEqual(a_hash.get_length(), 5)

        self.assertTrue(a_hash.exists_member('e'))
        del a_hash['e']
        self.assertFalse(a_hash.exists_member('e'))
        self.assertEqual(a_hash.delete_by_key('e'), 0)
        self.assertEqual(a_hash.delete_by_key(['a', 'b']), 2)

    def test__increase_member__success(self):
        b_hash = Hash(main_key='b_hash', rdb=self.rdb)
        self.assertEqual(b_hash.increase_member('a', 10), 10)
        self.assertEqual(b_hash.increase_member('a', 100), 110)
