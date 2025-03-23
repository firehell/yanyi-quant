#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import websocket
import json
import time
import threading
from app.utils.logger import setup_logger
from app.config.config import POLYGON_CONFIG

logger = setup_logger('polygon_api')

class PolygonAPI:
    """Polygon API工具类，用于与Polygon API交互获取实时和历史数据"""
    
    def __init__(self):
        """初始化Polygon API工具类"""
        self.api_key = POLYGON_CONFIG['api_key']
        self.ws_url = POLYGON_CONFIG['ws_url']
        self.rest_url = POLYGON_CONFIG['rest_url']
        self.ws = None
        self.ws_connected = False
        self.ws_thread = None
        self.callbacks = {
            'trades': [],
            'quotes': [],
            'aggs': [],
            'connection': [],
            'error': []
        }
    
    def connect_websocket(self):
        """连接Polygon WebSocket"""
        def on_open(ws):
            """WebSocket连接打开时的回调"""
            logger.info("WebSocket连接已建立")
            self.ws_connected = True
            auth_msg = {
                "action": "auth",
                "params": self.api_key
            }
            ws.send(json.dumps(auth_msg))
            
            # 通知连接已建立
            for callback in self.callbacks['connection']:
                callback({'status': 'connected'})
        
        def on_message(ws, message):
            """接收WebSocket消息的回调"""
            try:
                data = json.loads(message)
                
                # 处理不同类型的消息
                for msg in data:
                    ev_type = msg.get('ev')
                    if ev_type == 'T':  # 成交数据
                        for callback in self.callbacks['trades']:
                            callback(msg)
                    elif ev_type == 'Q':  # 报价数据
                        for callback in self.callbacks['quotes']:
                            callback(msg)
                    elif ev_type == 'AM':  # 聚合数据
                        for callback in self.callbacks['aggs']:
                            callback(msg)
            except Exception as e:
                logger.error(f"处理WebSocket消息时出错: {e}")
                for callback in self.callbacks['error']:
                    callback({'error': str(e), 'message': message})
        
        def on_error(ws, error):
            """WebSocket错误回调"""
            logger.error(f"WebSocket错误: {error}")
            for callback in self.callbacks['error']:
                callback({'error': str(error)})
        
        def on_close(ws, close_status_code, close_reason):
            """WebSocket连接关闭时的回调"""
            logger.info(f"WebSocket连接已关闭: {close_status_code} - {close_reason}")
            self.ws_connected = False
            for callback in self.callbacks['connection']:
                callback({'status': 'disconnected'})
        
        def run_websocket():
            """在单独的线程中运行WebSocket"""
            while True:
                try:
                    # 创建WebSocket连接
                    websocket.enableTrace(False)
                    self.ws = websocket.WebSocketApp(
                        f"{self.ws_url}",
                        on_open=on_open,
                        on_message=on_message,
                        on_error=on_error,
                        on_close=on_close
                    )
                    self.ws.run_forever()
                    
                    # 如果连接关闭，等待一段时间后重连
                    logger.info("WebSocket连接断开，5秒后尝试重连...")
                    time.sleep(5)
                except Exception as e:
                    logger.error(f"WebSocket线程错误: {e}")
                    time.sleep(5)
        
        # 在单独的线程中启动WebSocket连接
        self.ws_thread = threading.Thread(target=run_websocket)
        self.ws_thread.daemon = True
        self.ws_thread.start()
    
    def subscribe(self, symbols, channels=None):
        """
        订阅股票数据
        
        Args:
            symbols (list): 股票代码列表
            channels (list, optional): 频道列表，例如：['T', 'Q', 'AM']，默认为['T']
                T: 成交数据
                Q: 报价数据
                AM: 分钟聚合数据
        """
        if not self.ws_connected:
            logger.warning("WebSocket尚未连接，无法订阅")
            return False
        
        if channels is None:
            channels = ['T']
        
        subscription_msg = {
            "action": "subscribe",
            "params": ",".join([f"{channel}.{symbol}" for channel in channels for symbol in symbols])
        }
        
        try:
            self.ws.send(json.dumps(subscription_msg))
            logger.info(f"已订阅: {subscription_msg}")
            return True
        except Exception as e:
            logger.error(f"订阅失败: {e}")
            return False
    
    def unsubscribe(self, symbols, channels=None):
        """
        取消订阅股票数据
        
        Args:
            symbols (list): 股票代码列表
            channels (list, optional): 频道列表，例如：['T', 'Q', 'AM']，默认为['T']
        """
        if not self.ws_connected:
            logger.warning("WebSocket尚未连接，无法取消订阅")
            return False
        
        if channels is None:
            channels = ['T']
        
        unsubscription_msg = {
            "action": "unsubscribe",
            "params": ",".join([f"{channel}.{symbol}" for channel in channels for symbol in symbols])
        }
        
        try:
            self.ws.send(json.dumps(unsubscription_msg))
            logger.info(f"已取消订阅: {unsubscription_msg}")
            return True
        except Exception as e:
            logger.error(f"取消订阅失败: {e}")
            return False
    
    def add_callback(self, event_type, callback):
        """
        添加回调函数
        
        Args:
            event_type (str): 事件类型，例如：'trades', 'quotes', 'aggs', 'connection', 'error'
            callback (function): 回调函数，接收一个参数（数据字典）
        """
        if event_type not in self.callbacks:
            logger.warning(f"不支持的事件类型: {event_type}")
            return False
        
        self.callbacks[event_type].append(callback)
        logger.info(f"已添加{event_type}事件的回调函数")
        return True
    
    def remove_callback(self, event_type, callback):
        """
        移除回调函数
        
        Args:
            event_type (str): 事件类型
            callback (function): 回调函数
        """
        if event_type not in self.callbacks:
            logger.warning(f"不支持的事件类型: {event_type}")
            return False
        
        if callback in self.callbacks[event_type]:
            self.callbacks[event_type].remove(callback)
            logger.info(f"已移除{event_type}事件的回调函数")
            return True
        else:
            logger.warning(f"回调函数未找到")
            return False
    
    def disconnect(self):
        """断开WebSocket连接"""
        if self.ws_connected and self.ws:
            self.ws.close()
            self.ws_connected = False
            logger.info("已断开WebSocket连接")
            return True
        else:
            logger.warning("WebSocket尚未连接，无需断开")
            return False
    
    def get_stock_aggs(self, symbol, multiplier, timespan, from_date, to_date):
        """
        获取股票聚合数据（REST API）
        
        Args:
            symbol (str): 股票代码
            multiplier (int): 时间单位的倍数
            timespan (str): 时间单位，例如：'minute', 'hour', 'day', 'week', 'month', 'quarter', 'year'
            from_date (str): 开始日期，格式：YYYY-MM-DD
            to_date (str): 结束日期，格式：YYYY-MM-DD
            
        Returns:
            dict: 包含股票聚合数据的字典
        """
        url = f"{self.rest_url}/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{from_date}/{to_date}?apiKey={self.api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK':
                return data
            else:
                logger.error(f"获取聚合数据失败: {data}")
                return {}
        except Exception as e:
            logger.error(f"调用REST API失败: {e}")
            return {}
    
    def get_stock_trades(self, symbol, date):
        """
        获取股票当日成交数据（REST API）
        
        Args:
            symbol (str): 股票代码
            date (str): 日期，格式：YYYY-MM-DD
            
        Returns:
            dict: 包含股票成交数据的字典
        """
        url = f"{self.rest_url}/v3/trades/{symbol}?timestamp={date}&apiKey={self.api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK':
                return data
            else:
                logger.error(f"获取成交数据失败: {data}")
                return {}
        except Exception as e:
            logger.error(f"调用REST API失败: {e}")
            return {}
    
    def get_stock_quotes(self, symbol, date):
        """
        获取股票当日报价数据（REST API）
        
        Args:
            symbol (str): 股票代码
            date (str): 日期，格式：YYYY-MM-DD
            
        Returns:
            dict: 包含股票报价数据的字典
        """
        url = f"{self.rest_url}/v3/quotes/{symbol}?timestamp={date}&apiKey={self.api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK':
                return data
            else:
                logger.error(f"获取报价数据失败: {data}")
                return {}
        except Exception as e:
            logger.error(f"调用REST API失败: {e}")
            return {} 