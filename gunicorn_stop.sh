#!/bin/bash

# 检查PID文件是否存在
if [ -f /tmp/gunicorn.pid ]; then
    # 杀死进程
    kill $(cat /tmp/gunicorn.pid)
    # 删除PID文件
    rm /tmp/gunicorn.pid
    echo "Gunicorn已停止"
else
    echo "未找到运行的Gunicorn进程"
fi