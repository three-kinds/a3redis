#!/usr/bin/env bash

# 运行这个脚本前，要先进入pod
# kubectl exec -it test-a3redis -- /bin/bash
# cd /a3redis

PACKAGE="a3redis"

PACKAGE_PATH="$(dirname "$0")/.."
export PYTHONPATH=$PYTHONPATH:$PACKAGE_PATH
cd $PACKAGE_PATH

coverage erase
coverage run --source=$PACKAGE -m unittest discover
coverage html --title="$PACKAGE coverage report"
# python -m webbrowser ./htmlcov/index.html
