#!/bin/bash
# 中国象棋游戏启动脚本

echo "================================"
echo "中国象棋 - Chinese Chess"
echo "================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python 3"
    echo "请安装 Python 3.8 或更高版本"
    exit 1
fi

# 检查 Pygame
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "警告: 未安装 Pygame"
    echo "正在安装 Pygame..."
    pip3 install pygame
    if [ $? -ne 0 ]; then
        echo "错误: Pygame 安装失败"
        exit 1
    fi
fi

echo "启动游戏..."
echo ""
python3 main.py
