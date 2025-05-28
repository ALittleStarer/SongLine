#!/bin/bash

PROJECT_DIR="/home/admin/django/letter_recorder"
PID_FILE="$PROJECT_DIR/run.pid"
LOG_FILE="$PROJECT_DIR/logs/run_$(date +%Y%m%d).log"

case "$1" in
    start)
        if [ -f $PID_FILE ]; then
            echo "服务已在运行 (PID: $(cat $PID_FILE))"
            exit 1
        fi
        cd $PROJECT_DIR
        nohup /usr/bin/python3 manage.py runserver 0.0.0.0:8000 > $LOG_FILE 2>&1 &
        # 使用精确匹配获取Python进程ID
        PID=$(pgrep -f "manage.py runserver 0.0.0.0:8000" | head -1)
        if [ -z "$PID" ]; then
            echo "进程启动失败"
            exit 1
        fi
        echo $PID > $PID_FILE
        echo "服务已启动 (PID: $(cat $PID_FILE))"
        ;;
    stop)
        if [ ! -f $PID_FILE ]; then
            echo "服务未运行"
            exit 1
        fi
        kill -9 $(cat $PID_FILE) && rm -f $PID_FILE
        echo "服务已停止"
        ;;
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    status)
        if [ -f $PID_FILE ]; then
            if ps -p $(cat $PID_FILE) > /dev/null; then
                echo "运行中 (PID: $(cat $PID_FILE))"
            else
                echo "PID文件存在但进程未运行"
                rm -f $PID_FILE
            fi
        else
            echo "服务未运行"
        fi
        ;;
    *)
        echo "使用方法: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac