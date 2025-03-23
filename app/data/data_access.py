#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import datetime
from app.data.db_utils import DBUtils
from app.utils.logger import setup_logger

logger = setup_logger('data_access')

class DataAccess:
    """数据访问层，提供历史数据和实时数据的统一访问接口"""
    
    @staticmethod
    def get_stock_data(symbol, start_date, end_date=None, interval='1m'):
        """
        获取股票历史数据
        
        Args:
            symbol (str): 股票代码
            start_date (str or datetime): 开始日期，格式：YYYY-MM-DD
            end_date (str or datetime, optional): 结束日期，格式：YYYY-MM-DD，默认为当天
            interval (str, optional): 数据周期，默认为1分钟 '1m'
            
        Returns:
            DataFrame: 包含股票历史数据的DataFrame
        """
        try:
            # 参数预处理
            if isinstance(start_date, str):
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            
            if end_date is None:
                end_date = datetime.datetime.now().date()
            elif isinstance(end_date, str):
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            
            # 构建SQL查询
            # 注意：这里的表名和字段名需要根据实际数据库结构进行调整
            if interval == '1m':
                table_name = 'stock_minute_data'
            elif interval == '1d':
                table_name = 'stock_daily_data'
            else:
                raise ValueError(f"不支持的数据周期: {interval}")
            
            sql = f"""
            SELECT * FROM {table_name}
            WHERE symbol = %s
              AND date >= %s
              AND date <= %s
            ORDER BY date, time
            """
            
            params = (symbol, start_date, end_date)
            
            # 执行查询
            df = DBUtils.query_to_dataframe(sql, params)
            
            if df.empty:
                logger.warning(f"未找到股票 {symbol} 在 {start_date} 至 {end_date} 期间的数据")
                return pd.DataFrame()
            
            # 处理时间戳
            if 'date' in df.columns and 'time' in df.columns:
                df['timestamp'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str))
                df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"获取股票历史数据失败: {e}")
            raise
    
    @staticmethod
    def get_latest_data(symbol):
        """
        获取股票最新数据
        
        Args:
            symbol (str): 股票代码
            
        Returns:
            dict: 包含股票最新数据的字典
        """
        try:
            # 构建SQL查询
            sql = """
            SELECT * FROM stock_minute_data
            WHERE symbol = %s
            ORDER BY date DESC, time DESC
            LIMIT 1
            """
            
            params = (symbol,)
            
            # 执行查询
            results = DBUtils.execute_query(sql, params)
            
            if not results:
                logger.warning(f"未找到股票 {symbol} 的最新数据")
                return {}
            
            return results[0]
            
        except Exception as e:
            logger.error(f"获取股票最新数据失败: {e}")
            raise
    
    @staticmethod
    def get_multiple_stocks_data(symbols, start_date, end_date=None, interval='1m'):
        """
        获取多只股票的历史数据
        
        Args:
            symbols (list): 股票代码列表
            start_date (str or datetime): 开始日期，格式：YYYY-MM-DD
            end_date (str or datetime, optional): 结束日期，格式：YYYY-MM-DD，默认为当天
            interval (str, optional): 数据周期，默认为1分钟 '1m'
            
        Returns:
            dict: 以股票代码为键，DataFrame为值的字典
        """
        result = {}
        for symbol in symbols:
            df = DataAccess.get_stock_data(symbol, start_date, end_date, interval)
            result[symbol] = df
        
        return result
    
    @staticmethod
    def save_data(df, table_name):
        """
        保存数据到数据库
        
        Args:
            df (DataFrame): 待保存的数据
            table_name (str): 表名
            
        Returns:
            int: 受影响的行数
        """
        try:
            # 将DataFrame转换为记录列表
            records = df.to_dict('records')
            
            if not records:
                logger.warning(f"没有数据需要保存到 {table_name}")
                return 0
            
            # 构建SQL语句
            columns = ', '.join(records[0].keys())
            placeholders = ', '.join(['%s'] * len(records[0]))
            
            sql = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders})
            """
            
            # 构建参数列表
            params_list = [tuple(record.values()) for record in records]
            
            # 执行批量插入
            affected_rows = DBUtils.execute_many(sql, params_list)
            
            logger.info(f"成功保存 {affected_rows} 条数据到 {table_name}")
            
            return affected_rows
            
        except Exception as e:
            logger.error(f"保存数据失败: {e}")
            raise 