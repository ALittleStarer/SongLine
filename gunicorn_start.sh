#!/bin/bash

# 进入项目目录
cd /home/admin/django/songline_recorder

# 使用系统Python3直接运行
/usr/bin/python3 -m gunicorn --bind 0.0.0.0:8000 \
songline_recorder.wsgi:application \
--pid /tmp/gunicorn.pid \
--daemon

echo "Gunicorn已通过$(/usr/bin/python3 -V)启动"