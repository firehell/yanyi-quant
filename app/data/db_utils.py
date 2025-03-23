#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import pandas as pd
from pymysql.cursors import DictCursor
import logging
from app.config.config import DB_CONFIG

logger = logging.getLogger(__name__)

class DBUtils:
    """数据库工具类，提供数据库连接和基本操作"""
    
    @staticmethod
    def get_connection():
        """获取数据库连接"""
        try:
            connection = pymysql.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG['database'],
                charset=DB_CONFIG['charset'],
                cursorclass=DictCursor
            )
            return connection
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise

    @staticmethod
    def execute_query(sql, params=None):
        """执行查询SQL，返回字典列表"""
        connection = None
        try:
            connection = DBUtils.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                result = cursor.fetchall()
                return result
        except Exception as e:
            logger.error(f"执行查询失败: {e}")
            raise
        finally:
            if connection:
                connection.close()

    @staticmethod
    def execute_many(sql, params_list):
        """执行批量操作"""
        connection = None
        try:
            connection = DBUtils.get_connection()
            with connection.cursor() as cursor:
                cursor.executemany(sql, params_list)
                connection.commit()
                return cursor.rowcount
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"执行批量操作失败: {e}")
            raise
        finally:
            if connection:
                connection.close()

    @staticmethod
    def execute_update(sql, params=None):
        """执行更新操作"""
        connection = None
        try:
            connection = DBUtils.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                connection.commit()
                return cursor.rowcount
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"执行更新操作失败: {e}")
            raise
        finally:
            if connection:
                connection.close()

    @staticmethod
    def query_to_dataframe(sql, params=None):
        """查询并转换为DataFrame"""
        try:
            results = DBUtils.execute_query(sql, params)
            df = pd.DataFrame(results)
            return df
        except Exception as e:
            logger.error(f"查询转DataFrame失败: {e}")
            raise 