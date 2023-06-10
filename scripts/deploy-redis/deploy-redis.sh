#!/bin/bash

# 可以使用minikube安装redis，简单
minikube start --image-mirror-country='cn' --kubernetes-version=v1.23.8
helm repo add bitnami https://charts.bitnami.com/bitnami

helm install redis-standalone bitnami/redis --values standalone_redis_values.yaml
helm install redis-sentinel bitnami/redis --values sentinel_redis_values.yaml
helm install redis-cluster bitnami/redis-cluster --values cluster_redis_values.yaml

# minikube设置可以mount本机目录
ip r g $(minikube ip)|awk '{print $3}'|head -n1|xargs sudo ufw allow in on
sudo ufw reload
minikube mount $HOME:/host
# 加载目标环境
kubectl apply -f test_a3redis_pod.yaml


# 如有需要，可以使用redis-cluster-proxy代理redis-cluster
# kubectl run redis-cluster-proxy --port=7777 --image kornrunner/redis-cluster-proxy:latest --command -- \
#   redis-cluster-proxy --auth 123456 --port 7777 redis-cluster:6379
