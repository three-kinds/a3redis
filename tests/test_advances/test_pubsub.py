# -*- coding: utf-8 -*-
import threading
import time
from ..base_redis_test_case import BaseRedisTestCase

from a3redis.advances import Publisher, Subscriber


class PubSubTestCase(BaseRedisTestCase):
    def test__single_listener_success(self):
        tc = self
        single_channel_name = "single_listener"
        test_message = single_channel_name + "message"

        class PublisherThread(threading.Thread):
            def __init__(self):
                super().__init__()
                self.publisher = Publisher(channel_name=single_channel_name, rdb=tc.rdb)

            def run(self) -> None:
                time.sleep(1)
                self.publisher.publish(test_message)

        class OneOffSubscriber(Subscriber):
            rdb = tc.rdb

            def on_message(self, channel_name: str, message: str):
                tc.assertEqual(single_channel_name, channel_name)
                tc.assertEqual(self._channel_name, channel_name)
                tc.assertEqual(message, test_message)
                self._should_break = True

        single_listener = OneOffSubscriber(channel_name=single_channel_name)
        publisher_thread = PublisherThread()
        publisher_thread.start()
        single_listener.start()

    def test__multi_listener_success(self):
        tc = self
        multi_channel_name = "multi_listener:"
        test_message = multi_channel_name + "message"

        class PublisherThread(threading.Thread):
            def __init__(self, index: int):
                super().__init__()
                self.publisher = Publisher(channel_name=multi_channel_name + str(index), rdb=tc.rdb)

            def run(self) -> None:
                time.sleep(2)
                self.publisher.publish(test_message)

        class MultiListener(Subscriber):
            rdb = tc.rdb
            listened_count = 0

            def on_message(self, channel_name: str, message: str):
                tc.assertTrue(channel_name.startswith(multi_channel_name))
                tc.assertEqual(message, test_message)
                self.listened_count += 1

                self._should_break = self.listened_count == 2

        multi_listener = MultiListener(channel_name=multi_channel_name + "*")
        for i in range(2):
            publisher_thread = PublisherThread(i)
            publisher_thread.start()
        multi_listener.start()
