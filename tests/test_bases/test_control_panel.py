# -*- coding: utf-8 -*-
from a3redis.bases import ControlPanel
from tests.base_redis_test_case import BaseRedisTestCase


class ControlPanelTestCase(BaseRedisTestCase):

    def test__info__success(self):
        control_panel = ControlPanel(rdb=self.rdb)
        self.assertGreater(
            len(control_panel.server_info), 0
        )
        self.assertGreater(
            len(control_panel.client_info), 0
        )
        self.assertGreater(
            len(control_panel.memory_info), 0
        )
        self.assertGreater(
            len(control_panel.cpu_info), 0
        )

    def test__flush_db__success(self):
        control_panel = ControlPanel(rdb=self.rdb)

        control_panel.flush_db()
        self.assertEqual(control_panel.get_key_count(), 0)

        control_panel.rdb.set('key', 'value')
        self.assertEqual(control_panel.get_key_count(), 1)

        control_panel.flush_db()
        self.assertEqual(control_panel.get_key_count(), 0)
