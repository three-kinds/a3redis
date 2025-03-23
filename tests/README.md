# Test

## 1. Deploy different types of Redis instances using helm.

```shell
helm repo add bitnami https://charts.bitnami.com/bitnami

cd deploy-redis
helm install standalone bitnami/redis --values standalone_redis_values.yaml
helm install sentinel bitnami/redis --values sentinel_redis_values.yaml
helm install cluster bitnami/redis-cluster --values cluster_redis_values.yaml
# Deploy test-a3redis pod
kubectl apply -f test_a3redis_pod.yaml

```

## 2. Prepare test environment.

```shell
# in the pyenv container
apt install -y make git sqlite3 vim

```

## 3. Run test cases.

```shell
git clone https://github.com/three-kinds/a3redis.git
cd a3redis

make init
make coverage
make test

```
