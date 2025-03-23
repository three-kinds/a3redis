# -*- coding: utf-8 -*-
import os
from a3redis.structures import String
from a3redis.advances import Script

from ..base_redis_test_case import BaseRedisTestCase


class ScriptTestCase(BaseRedisTestCase):
    def test__script__success(self):
        for i in range(2):
            String(main_key="test_{}".format(i), rdb=self.rdb).set(i + 10)

        fd = open(os.path.join(os.path.dirname(__file__), "test_script.lua"), "r")
        lua_content = fd.read()
        fd.close()

        script = Script(lua_content=lua_content, rdb=self.rdb)
        result = script.execute(key_list=[], value_list=[0, 1])

        for i in range(2):
            self.assertEqual(result[i], i)
