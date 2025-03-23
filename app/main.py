#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import logging
from app.utils.logger import setup_logger
from app.data.data_access import DataAccess
from app.data.data_cleaner import DataCleaner
from app.data.polygon_api import PolygonAPI

logger = setup_logger('main')

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='美股日内交易辅助系统')
    parser.add_argument('--clean', action='store_true', help='清洗历史数据')
    parser.add_argument('--symbol', type=str, help='股票代码')
    parser.add_argument('--start-date', type=str, help='开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, help='结束日期 (YYYY-MM-DD)')
    parser.add_argument('--realtime', action='store_true', help='启动实时数据处理')
    return parser.parse_args()

def clean_historical_data(symbol, start_date, end_date):
    """清洗历史数据"""
    logger.info(f"开始清洗股票 {symbol} 从 {start_date} 到 {end_date} 的历史数据")
    
    # 获取历史数据
    data_access = DataAccess()
    df = data_access.get_stock_data(symbol, start_date, end_date)
    
    if df.empty:
        logger.warning(f"未找到股票 {symbol} 在指定日期范围内的数据")
        return
    
    logger.info(f"获取到 {len(df)} 行历史数据")
    
    # 清洗数据
    cleaner = DataCleaner()
    cleaned_df = cleaner.clean_stock_data(df)
    
    logger.info(f"清洗后剩余 {len(cleaned_df)} 行数据")
    
    # 保存清洗后的数据
    # 这里需要根据实际数据库结构进行调整
    # 可以保存到新表，也可以更新原表
    # 示例：保存到新表
    table_name = 'stock_minute_data_cleaned'
    affected_rows = data_access.save_data(cleaned_df, table_name)
    
    logger.info(f"保存了 {affected_rows} 行数据到 {table_name}")

def start_realtime_processing():
    """启动实时数据处理"""
    logger.info("启动实时数据处理")
    
    # 创建Polygon API实例
    polygon_api = PolygonAPI()
    
    # 自定义回调函数，处理实时数据
    def on_trade(trade_data):
        logger.debug(f"收到成交数据: {trade_data}")
        # TODO: 添加实时数据处理逻辑
    
    def on_quote(quote_data):
        logger.debug(f"收到报价数据: {quote_data}")
        # TODO: 添加实时数据处理逻辑
    
    def on_agg(agg_data):
        logger.debug(f"收到聚合数据: {agg_data}")
        # TODO: 添加实时数据处理逻辑
    
    def on_connection(connection_data):
        status = connection_data.get('status')
        if status == 'connected':
            logger.info("WebSocket连接已建立")
            # 连接建立后订阅股票
            symbols = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB']  # 示例股票列表
            channels = ['T', 'Q', 'AM']
            polygon_api.subscribe(symbols, channels)
        elif status == 'disconnected':
            logger.info("WebSocket连接已断开")
    
    def on_error(error_data):
        logger.error(f"WebSocket错误: {error_data}")
    
    # 添加回调函数
    polygon_api.add_callback('trades', on_trade)
    polygon_api.add_callback('quotes', on_quote)
    polygon_api.add_callback('aggs', on_agg)
    polygon_api.add_callback('connection', on_connection)
    polygon_api.add_callback('error', on_error)
    
    # 连接WebSocket
    polygon_api.connect_websocket()
    
    try:
        # 保持程序运行
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在退出...")
        polygon_api.disconnect()

def main():
    """主函数"""
    args = parse_args()
    
    if args.clean:
        if not args.symbol or not args.start_date:
            logger.error("清洗数据需要指定股票代码和开始日期")
            return 1
        clean_historical_data(args.symbol, args.start_date, args.end_date)
    elif args.realtime:
        start_realtime_processing()
    else:
        logger.error("请指定要执行的操作 (--clean 或 --realtime)")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())