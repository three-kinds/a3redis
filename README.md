# a3redis

English | [简体中文](README_ZH.md)

`a3redis` is a simple wrapper around `redis-py` to make it easier to use.

## 1. Introduction

* When logically compatible, the Redis service type (standalone, sentinel, or cluster) can be switched by only modifying the configuration without changing the code.
* You can configure multiple Redis services of different types at the same time; if no Redis service configuration is specified, `redis://localhost:6379/0` will be used by default.
* Provides class forms of commonly used data structures for ease of use.

## 2. Usage

## Install

```shell
pip install a3redis

```

## Examples

```python
CONF = {
    "standalone": {
        "mode": "standalone",
        "init": {
            "host": "standalone-redis-master",
            "port": 6379,
            "db": 0,
            "password": "standalone",
            "decode_responses": True
        }
    },
    "sentinel": {
        "mode": "sentinel",
        "init": {
            "sentinels": [
                ["sentinel-redis-node-0.sentinel-redis-headless", 26379],
                ["sentinel-redis-node-1.sentinel-redis-headless", 26379],
                ["sentinel-redis-node-2.sentinel-redis-headless", 26379]
            ],
            "sentinel_kwargs": {
                "password": "sentinel"
            },
            "password": "sentinel",
            "db": 1,
            "decode_responses": True
        },
        "runtime": {
            "service_name": "my-master"
        }
    },
    "cluster": {
        "mode": "cluster",
        "init": {
            "host": "cluster-redis-cluster",
            "port": 6379,
            "password": "cluster",
            "decode_responses": True
        }
    }
}


from a3redis.bases import RedisClientFactory, RedisMode
from a3redis.structures import Hash


class User(Hash):
    main_key = 'user:{id}'
    _hkey_username = 'username'

    def get_username(self) -> str:
        return self.get_member_by_key(self._hkey_username)

    def set_username(self, username: str):
        self.set_member(self._hkey_username, username)


if __name__ == '__main__':
    RedisClientFactory.init_redis_clients(conf=CONF)

    localhost_anonymous_rdb = None
    standalone_rdb = RedisClientFactory.get_rdb(RedisMode.Standalone)
    sentinel_rdb = RedisClientFactory.get_rdb(RedisMode.Sentinel)
    cluster_rdb = RedisClientFactory.get_rdb(RedisMode.Cluster)
    
    for rdb in [localhost_anonymous_rdb, standalone_rdb, sentinel_rdb, cluster_rdb]:
        user = User(id="123", rdb=rdb)
        user.set_username("tom")
        user.get_username()
        user.delete()

```
