#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from app.utils.logger import setup_logger
from app.config.config import DATA_CLEANING_CONFIG, TRADING_HOURS

logger = setup_logger('data_cleaner')

class DataCleaner:
    """数据清洗工具类，用于处理数据中的缺失值、异常值等问题"""
    
    @staticmethod
    def clean_stock_data(df):
        """
        清洗股票数据
        
        Args:
            df (DataFrame): 包含股票数据的DataFrame
            
        Returns:
            DataFrame: 清洗后的DataFrame
        """
        if df.empty:
            logger.warning("输入数据为空，无需清洗")
            return df
        
        # 复制一份数据，避免修改原始数据
        cleaned_df = df.copy()
        
        # 执行清洗操作
        cleaned_df = DataCleaner._handle_missing_values(cleaned_df)
        cleaned_df = DataCleaner._remove_abnormal_price_changes(cleaned_df)
        cleaned_df = DataCleaner._remove_abnormal_volume(cleaned_df)
        cleaned_df = DataCleaner._check_trading_hours(cleaned_df)
        
        # 记录清洗结果
        removed_rows = len(df) - len(cleaned_df)
        if removed_rows > 0:
            logger.info(f"清洗过程中移除了 {removed_rows} 行数据")
        
        return cleaned_df
    
    @staticmethod
    def _handle_missing_values(df):
        """处理缺失值"""
        # 检查必要列是否存在
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"数据缺少必要列：{col}")
                raise ValueError(f"数据缺少必要列：{col}")
        
        # 填充缺失值
        for col in required_columns:
            if df[col].isna().any():
                # 对于价格列，使用前向填充
                if col in ['open', 'high', 'low', 'close']:
                    df[col] = df[col].fillna(method='ffill')
                # 对于成交量，填充为0
                elif col == 'volume':
                    df[col] = df[col].fillna(0)
        
        # 检查是否有连续缺失的数据
        max_missing = DATA_CLEANING_CONFIG['max_missing_minutes']
        
        # 假设时间戳是索引，并且按分钟排序
        # 重置索引，以便我们可以使用时间戳列
        if isinstance(df.index, pd.DatetimeIndex):
            df = df.reset_index()
            timestamp_col = 'index'
        else:
            timestamp_col = 'timestamp'
        
        # 计算时间差（分钟）
        if timestamp_col in df.columns:
            df['time_diff'] = df[timestamp_col].diff().dt.total_seconds() / 60
            
            # 标记连续缺失超过max_missing分钟的数据
            dates_to_remove = df.loc[df['time_diff'] > max_missing, 'date'].unique()
            
            if len(dates_to_remove) > 0:
                logger.info(f"发现连续缺失超过{max_missing}分钟的日期：{dates_to_remove}")
                df = df[~df['date'].isin(dates_to_remove)]
            
            # 删除临时列
            df = df.drop(columns=['time_diff'])
            
            # 恢复索引
            if timestamp_col == 'index':
                df = df.set_index('index')
        
        return df
    
    @staticmethod
    def _remove_abnormal_price_changes(df):
        """移除异常价格变化"""
        abnormal_pct = DATA_CLEANING_CONFIG['abnormal_price_change_pct']
        
        # 计算收盘价的百分比变化
        df['close_pct_change'] = df['close'].pct_change().abs()
        
        # 标记异常价格变化
        abnormal_mask = df['close_pct_change'] > abnormal_pct
        abnormal_count = abnormal_mask.sum()
        
        if abnormal_count > 0:
            logger.info(f"发现 {abnormal_count} 条异常价格变化（变化率 > {abnormal_pct * 100}%）")
            df = df[~abnormal_mask]
        
        # 删除临时列
        df = df.drop(columns=['close_pct_change'])
        
        return df
    
    @staticmethod
    def _remove_abnormal_volume(df):
        """移除异常成交量"""
        multiplier = DATA_CLEANING_CONFIG['abnormal_volume_multiplier']
        window = DATA_CLEANING_CONFIG['volume_window_minutes']
        
        # 计算成交量的滚动平均值
        df['volume_rolling_mean'] = df['volume'].rolling(window=window, min_periods=1).mean()
        
        # 标记异常成交量
        abnormal_mask = df['volume'] > df['volume_rolling_mean'] * multiplier
        abnormal_count = abnormal_mask.sum()
        
        if abnormal_count > 0:
            logger.info(f"发现 {abnormal_count} 条异常成交量（> 平均值的 {multiplier} 倍）")
            df = df[~abnormal_mask]
        
        # 删除临时列
        df = df.drop(columns=['volume_rolling_mean'])
        
        return df
    
    @staticmethod
    def _check_trading_hours(df):
        """检查交易时间一致性"""
        # 提取交易时间（假设有time列或者可以从timestamp提取）
        if 'time' in df.columns:
            # 转换time列为字符串格式，便于比较
            df['time_str'] = df['time'].astype(str)
        elif 'timestamp' in df.columns:
            # 从timestamp提取时间部分
            df['time_str'] = df['timestamp'].dt.strftime('%H:%M')
        elif isinstance(df.index, pd.DatetimeIndex):
            # 从索引提取时间部分
            df['time_str'] = df.index.strftime('%H:%M')
        else:
            logger.warning("无法提取交易时间信息，跳过交易时间一致性检查")
            return df
        
        # 获取正常交易时间范围
        start_time = TRADING_HOURS['regular']['start']
        end_time = TRADING_HOURS['regular']['end']
        
        # 检查交易时间是否在正常范围内
        time_mask = (df['time_str'] >= start_time) & (df['time_str'] <= end_time)
        out_of_range_count = (~time_mask).sum()
        
        if out_of_range_count > 0:
            logger.info(f"发现 {out_of_range_count} 条交易时间不在正常范围内的数据")
            # 是否过滤掉这些数据取决于需求，这里我们保留
            # df = df[time_mask]
        
        # 删除临时列
        df = df.drop(columns=['time_str'])
        
        return df 