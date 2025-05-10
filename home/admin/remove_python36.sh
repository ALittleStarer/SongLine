#!/bin/bash

# 查看已安装的python3.6相关包
rpm -qa | grep 'python3.6'

# 卸载python3.6核心包（需要root权限）
sudo yum remove -y \
python36-libs-3.6.8* \
python36-devel-3.6.8* \
python36-setuptools-36.2.7* \
python36-pip-9.0.3*

# 清理残留文件
sudo find /usr/local/ -name "*python3.6*" -exec rm -rf {} +
sudo rm -rf /usr/bin/python3.6*

# 验证系统默认python版本
python3 --version