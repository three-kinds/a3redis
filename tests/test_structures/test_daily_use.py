# -*- coding: utf-8 -*-
import random
from unittest import TestCase
from a3redis.bases import RedisClientFactory, RedisMode
from a3redis.structures import Hash, List
from tests.base_redis_test_case import ALL_CONF


class T(TestCase):
    def test_daily_use(self):
        # load all redis server
        RedisClientFactory.init_redis_clients(ALL_CONF)

        class MessageList(List):
            rdb_conf_name = RedisMode.Cluster
            main_key = "message_list"

        message_list = MessageList()
        message_list.delete()
        self.assertEqual(message_list.exists(), False)

        message_list.right_push("message-1")
        self.assertEqual(message_list.get_length(), 1)
        message_list.delete()

    def test_different_server_mode(self):
        class User(Hash):
            main_key = "user:{id}"
            _hkey_username = "username"

            def get_username(self) -> str:
                return self.get_member_by_key(self._hkey_username)

            def set_username(self, username: str):
                self.set_member(self._hkey_username, username)

        tom_id = str(random.randint(10000, 9999999))
        # load all redis server
        RedisClientFactory.init_redis_clients(ALL_CONF)

        localhost_anonymous_rdb = None
        standalone_rdb = RedisClientFactory.get_rdb(RedisMode.Standalone)
        sentinel_rdb = RedisClientFactory.get_rdb(RedisMode.Sentinel)
        cluster_rdb = RedisClientFactory.get_rdb(RedisMode.Cluster)

        for rdb in [localhost_anonymous_rdb, standalone_rdb, sentinel_rdb, cluster_rdb]:
            tom = User(id=tom_id, rdb=rdb)
            tom_name = str(random.randint(10000, 9999999))
            tom.set_username(tom_name)
            self.assertEqual(tom.get_username(), tom_name)
            tom.delete()
            self.assertFalse(tom.exists())
