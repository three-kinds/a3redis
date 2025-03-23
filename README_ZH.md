# a3redis

[English](README.md) | 简体中文

`a3redis` 对 `redis-py` 做了简单的封装，目的是用起来更简单。

## 1. 简介

* 在逻辑兼容的情况下，可以通过不修改代码只修改配置的方式，切换 redis 的服务类型：单体、哨兵 或 集群
* 可以同时配置多个、不同类型的 redis 服务；如果没有指定 redis 服务配置，默认使用 `redis://localhost:6379/0`
* 提供常用数据结构的class形式，便于使用

## 2. 使用

## 安装

```shell
pip install a3redis

```

## 样例

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
