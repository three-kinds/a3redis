# -*- coding: utf-8 -*-
from a3redis.structures import SortedSet
from ..base_redis_test_case import BaseRedisTestCase


class SortedSetTestCase(BaseRedisTestCase):
    def test__add__success(self):
        ss = SortedSet(main_key="test_sorted_set", rdb=self.rdb)
        self.assertEqual(ss.add("1", 1), 1)
        self.assertEqual(ss.add("1", 1), 0)
        # get_score
        self.assertEqual(ss.add("2", 2, only_add=True), 1)
        self.assertEqual(ss.add("2", 3, only_add=True), 0)
        self.assertEqual(ss.get_score("2"), 2)

        self.assertEqual(ss.add("3", 3, only_update=True), 0)
        self.assertEqual(ss.get_score("3"), None)

        self.assertEqual(ss.add_list({"7": 7, "8": 8, "9": 9}), 3)
        self.assertEqual(ss.add_list({"7": 17, "8": 18, "9": 9}), 0)
        self.assertEqual(ss.add_list({"7": 27, "8": 28, "9": 9}, change_return=True), 2)

    def test__get_length__success(self):
        ss = SortedSet(main_key="test_sorted_set", rdb=self.rdb)
        ss.add_list({"7": 7, "8": 8, "9": 9})
        self.assertEqual(ss.get_length(), 3)

    def test__increase_member__success(self):
        ss = SortedSet(main_key="test_sorted_set", rdb=self.rdb)
        ss.add("1", 1)
        self.assertEqual(ss.increase_member("1", 2), 3.0)
        self.assertEqual(ss.increase_member("1", 2), 5.0)
        self.assertEqual(ss.get_score("1"), 5.0)

    def test__get_count__success(self):
        ss = SortedSet(main_key="test_sorted_set", rdb=self.rdb)
        for i in range(5):
            ss.add(str(i), i)

        self.assertEqual(ss.get_count_between_scores(1, 2), 2)
        self.assertEqual(ss.get_count_between_scores("(1", 2), 1)
        self.assertEqual(ss.get_count_between_scores("-inf", "+inf"), 5)
        self.assertEqual(ss.get_count_between_members("[1", "[2"), 2)
        self.assertEqual(ss.get_count_between_members("(1", "[2"), 1)
        self.assertEqual(ss.get_count_between_members("-", "+"), 5)

    def test__get_member_list__success(self):
        ss = SortedSet(main_key="test_sorted_set", rdb=self.rdb)
        for i in range(5):
            ss.add(str(i), i)

        self.assertEqual(ss.get_member_list(1, 2), ["1", "2"])
        self.assertEqual(ss.get_member_list(1, 2, with_scores=True), [("1", 1.0), ("2", 2.0)])
        self.assertEqual(ss.get_member_list(1, 2, with_scores=True, score_cast_func=int), [("1", 1), ("2", 2)])
        self.assertEqual(ss.get_member_list(1, 2, desc=True), ["3", "2"])
        # get_member_list_between_scores
        self.assertEqual(ss.get_member_list_between_scores(1, 2), ["1", "2"])
        self.assertEqual(ss.get_member_list_between_scores(1, 2, offset=0, count=1), ["1"])
        self.assertEqual(ss.get_member_list_between_scores(1, 2, desc=True), ["2", "1"])
        # get_member_list_between_members
        self.assertEqual(ss.get_member_list_between_members("[1", "[2"), ["1", "2"])
        self.assertEqual(ss.get_member_list_between_members("[1", "[2", desc=True), ["2", "1"])

    def test__get_rank__success(self):
        ss = SortedSet(main_key="test_sorted_set", rdb=self.rdb)
        for i in range(5):
            ss.add(str(i), i)

        self.assertEqual(ss.get_rank("0"), 0)
        self.assertEqual(ss.get_rank("4", desc=True), 0)

    def test__pop__success(self):
        ss = SortedSet(main_key="test_sorted_set", rdb=self.rdb)
        for i in range(5):
            ss.add(str(i), i)

        self.assertEqual(ss.pop_max(1), [("4", 4.0)])
        self.assertEqual(ss.pop_max(2), [("3", 3.0), ("2", 2.0)])
        self.assertEqual(ss.pop_min(1), [("0", 0.0)])

        self.assertEqual(ss.block_pop_max(), ("1", 1.0))
        self.assertEqual(ss.block_pop_min(1), None)
        ss.add("1", 1)
        self.assertEqual(ss.block_pop_min(1), ("1", 1.0))

    def test__remove_member__success(self):
        ss = SortedSet(main_key="test_sorted_set", rdb=self.rdb)
        for i in range(5):
            ss.add(str(i), i)

        self.assertEqual(ss.remove_member("4"), 1)
        self.assertEqual(ss.remove_member("4"), 0)
        # remove_member_list_between_scores
        self.assertEqual(ss.remove_member_list_between_scores("-inf", "+inf"), 4)

        for i in range(5):
            ss.add(str(i), i)
        # remove_member_list_between_members
        self.assertEqual(ss.remove_member_list_between_members("-", "+"), 5)
        for i in range(5):
            ss.add(str(i), i)
        # remove_member_list_between_ranks
        self.assertEqual(ss.remove_member_list_between_ranks(0, 5), 5)
