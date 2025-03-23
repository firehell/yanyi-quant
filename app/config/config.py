#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'password',  # 请修改为实际密码
    'database': 'yanyi_quant',  # 请修改为实际数据库名
    'charset': 'utf8mb4'
}

# Polygon API配置
POLYGON_CONFIG = {
    'api_key': '1c8e3e1a-7f13-4a88-a436-62a01886e16f',  # 从getdata.py中提取的API密钥
    'ws_url': 'wss://socket.polygon.io/stocks',
    'rest_url': 'https://api.polygon.io'
}

# 数据清洗配置
DATA_CLEANING_CONFIG = {
    'max_missing_minutes': 5,  # 连续缺失超过5分钟的数据将被删除
    'abnormal_price_change_pct': 0.05,  # 价格波动超过5%视为异常
    'abnormal_volume_multiplier': 10,  # 成交量超过过去M分钟平均成交量的10倍视为异常
    'volume_window_minutes': 30  # 计算成交量异常的时间窗口（M分钟）
}

# 股票交易时间配置（美东时间）
TRADING_HOURS = {
    'regular': {
        'start': '09:30',
        'end': '16:00'
    },
    'pre_market': {
        'start': '04:00',
        'end': '09:30'
    },
    'after_hours': {
        'start': '16:00',
        'end': '20:00'
    }
}

# 日志配置
LOG_CONFIG = {
    'log_level': 'INFO',
    'log_dir': 'logs/',
    'file_name': 'yanyi_quant.log'
} 