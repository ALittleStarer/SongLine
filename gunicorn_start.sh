#!/bin/bash

# 进入项目目录
cd /home/admin/django/letter_recorder

# 启动Gunicorn
gunicorn --bind 0.0.0.0:8000 letter_recorder.wsgi:application --pid /tmp/gunicorn.pid --daemon

echo "Gunicorn已启动，PID存储在/tmp/gunicorn.pid"