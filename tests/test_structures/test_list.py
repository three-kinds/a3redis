# -*- coding: utf-8 -*-
from a3redis.structures import List
from ..base_redis_test_case import BaseRedisTestCase


class ListTestCase(BaseRedisTestCase):
    def test__push_pop__success(self):
        a_list = List(main_key="a_pp_list", rdb=self.rdb)
        b_list = List(main_key="b_pp_list", rdb=self.rdb)

        a_list.right_push("0", need_exists=True)
        b_list.left_push("9", need_exists=True)
        self.assertEqual(a_list.get_length(), 0)
        self.assertEqual(b_list.get_length(), 0)

        a_list.right_push("0")
        b_list.left_push("9")
        self.assertEqual(a_list.get_length(), 1)
        self.assertEqual(b_list.get_length(), 1)

        a_list.right_push("1", need_exists=True)
        b_list.left_push("8", need_exists=True)
        self.assertEqual(a_list.get_length(), 2)
        self.assertEqual(b_list.get_length(), 2)

        self.assertEqual(a_list.get_all_members(), ["0", "1"])
        self.assertEqual(b_list.get_member_by_index(1), "9")

        self.assertEqual(a_list.left_pop(), "0")
        self.assertEqual(b_list.right_pop(), "9")

        self.assertEqual(a_list.get_length(), 1)
        self.assertEqual(b_list.get_length(), 1)

    def test__block_pop__success(self):
        a_list = List(main_key="a_bp_list", rdb=self.rdb)
        b_list = List(main_key="b_bp_list", rdb=self.rdb)

        a_list.right_push(["a", "b", "c"])
        b_list.left_push(["3", "2", "1"])

        self.assertEqual(a_list.block_right_pop(), "c")
        self.assertEqual(b_list.block_left_pop(), "1")

        self.assertEqual(a_list.get_length(), b_list.get_length())

        self.assertEqual(a_list.right_pop_left_push(b_list.main_key), "b")
        self.assertEqual(a_list.block_right_pop_left_push(b_list.main_key), "a")

        self.assertEqual(a_list.block_right_pop(1), None)

    def test__remove_member__success(self):
        a_list = List(main_key="a_rm_list", rdb=self.rdb)
        a_list.right_push(["a", "b", "a", "b", "c", "d"])

        self.assertEqual(a_list.remove_member("a"), 2)
        self.assertEqual(a_list.remove_member("d"), 1)
        self.assertEqual(a_list.get_length(), 3)

        self.assertEqual(a_list.remove_member("b", 1), 1)
        self.assertEqual(a_list.get_all_members(), ["b", "c"])
