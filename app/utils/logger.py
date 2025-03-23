#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import time
from logging.handlers import RotatingFileHandler
from app.config.config import LOG_CONFIG

def setup_logger(name=None):
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称，默认为root
        
    Returns:
        logger: 日志记录器实例
    """
    # 创建日志目录（如果不存在）
    log_dir = LOG_CONFIG['log_dir']
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 获取或创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_CONFIG['log_level']))
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 创建滚动文件处理器
    log_file = os.path.join(log_dir, LOG_CONFIG['file_name'])
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    
    # 设置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 