# -*- coding: utf-8 -*-
from a3redis.structures import Set
from ..base_redis_test_case import BaseRedisTestCase


class SetTestCase(BaseRedisTestCase):
    def test__add_pop__success(self):
        c_set = Set(main_key="c_set", rdb=self.rdb)

        c_set.add_member("a")
        self.assertEqual(c_set.pop(), "a")

        c_set.add_member(["b", "c"])
        self.assertEqual(c_set.get_all_members(), {"b", "c"})

        self.assertTrue(c_set.is_member("c"))
        self.assertEqual(c_set.remove_member("c"), 1)
        self.assertFalse(c_set.is_member("c"))

        self.assertEqual(c_set.remove_member(["c", "b"]), 1)

    def test__move__success(self):
        a_set = Set(main_key="a_set", rdb=self.rdb)
        b_set = Set(main_key="b_set", rdb=self.rdb)

        a_set.add_member(["a", "b", "c"])
        b_set.add_member(["1", "2", "3"])

        self.assertTrue(a_set.move_to(b_set.main_key, "c"))
        self.assertEqual(a_set.get_length(), 2)
        self.assertEqual(b_set.get_length(), 4)
