package main

import (
	"encoding/json"
	"fmt"
	"log"
	"sync"
	"time"

	"github.com/gorilla/websocket"
)

// WebSocketClient WebSocket客户端
type WebSocketClient struct {
	conn     *websocket.Conn
	url      string
	apiKey   string
	logger   *log.Logger
	mu       sync.Mutex
	isAlive  bool
	handlers map[string][]func([]byte)
}

// NewWebSocketClient 创建新的WebSocket客户端
func NewWebSocketClient(url string, apiKey string, logger *log.Logger) *WebSocketClient {
	return &WebSocketClient{
		url:      url,
		apiKey:   apiKey,
		logger:   logger,
		isAlive:  false,
		handlers: make(map[string][]func([]byte)),
	}
}

// Connect 连接WebSocket服务器
func (c *WebSocketClient) Connect() error {
	c.mu.Lock()
	defer c.mu.Unlock()

	if c.isAlive {
		return nil
	}

	c.logger.Printf("正在连接WebSocket服务器: %s", c.url)

	// 连接WebSocket服务器
	conn, _, err := websocket.DefaultDialer.Dial(c.url, nil)
	if err != nil {
		return fmt.Errorf("连接WebSocket服务器失败: %v", err)
	}

	c.conn = conn
	c.isAlive = true

	// 发送认证消息
	authMsg := map[string]interface{}{
		"action": "auth",
		"params": c.apiKey,
	}

	err = c.sendJSON(authMsg)
	if err != nil {
		c.conn.Close()
		c.isAlive = false
		return fmt.Errorf("发送认证消息失败: %v", err)
	}

	// 启动消息接收协程
	go c.receiveMessages()

	// 启动心跳检测协程
	go c.heartbeat()

	c.logger.Println("WebSocket连接成功")
	return nil
}

// Subscribe 订阅股票数据
func (c *WebSocketClient) Subscribe(symbols []string, channels []string) error {
	if !c.isAlive {
		return fmt.Errorf("WebSocket未连接")
	}

	if len(channels) == 0 {
		channels = []string{"T"}
	}

	// 构建订阅参数
	var params []string
	for _, channel := range channels {
		for _, symbol := range symbols {
			params = append(params, fmt.Sprintf("%s.%s", channel, symbol))
		}
	}

	// 发送订阅消息
	subMsg := map[string]interface{}{
		"action": "subscribe",
		"params": params,
	}

	err := c.sendJSON(subMsg)
	if err != nil {
		return fmt.Errorf("发送订阅消息失败: %v", err)
	}

	c.logger.Printf("已订阅: %v", params)
	return nil
}

// Unsubscribe 取消订阅股票数据
func (c *WebSocketClient) Unsubscribe(symbols []string, channels []string) error {
	if !c.isAlive {
		return fmt.Errorf("WebSocket未连接")
	}

	if len(channels) == 0 {
		channels = []string{"T"}
	}

	// 构建取消订阅参数
	var params []string
	for _, channel := range channels {
		for _, symbol := range symbols {
			params = append(params, fmt.Sprintf("%s.%s", channel, symbol))
		}
	}

	// 发送取消订阅消息
	unsubMsg := map[string]interface{}{
		"action": "unsubscribe",
		"params": params,
	}

	err := c.sendJSON(unsubMsg)
	if err != nil {
		return fmt.Errorf("发送取消订阅消息失败: %v", err)
	}

	c.logger.Printf("已取消订阅: %v", params)
	return nil
}

// AddHandler 添加消息处理器
func (c *WebSocketClient) AddHandler(eventType string, handler func([]byte)) {
	c.mu.Lock()
	defer c.mu.Unlock()

	if _, ok := c.handlers[eventType]; !ok {
		c.handlers[eventType] = []func([]byte){}
	}

	c.handlers[eventType] = append(c.handlers[eventType], handler)
}

// Disconnect 断开WebSocket连接
func (c *WebSocketClient) Disconnect() error {
	c.mu.Lock()
	defer c.mu.Unlock()

	if !c.isAlive {
		return nil
	}

	c.logger.Println("断开WebSocket连接")
	err := c.conn.Close()
	c.isAlive = false
	return err
}

// IsConnected 检查是否已连接
func (c *WebSocketClient) IsConnected() bool {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.isAlive
}

// 发送JSON消息
func (c *WebSocketClient) sendJSON(v interface{}) error {
	c.mu.Lock()
	defer c.mu.Unlock()

	return c.conn.WriteJSON(v)
}

// 接收并处理消息
func (c *WebSocketClient) receiveMessages() {
	for {
		_, message, err := c.conn.ReadMessage()
		if err != nil {
			c.logger.Printf("读取消息失败: %v", err)
			c.reconnect()
			return
		}

		// 解析消息
		var data []map[string]interface{}
		err = json.Unmarshal(message, &data)
		if err != nil {
			c.logger.Printf("解析消息失败: %v", err)
			continue
		}

		// 处理消息
		for _, msg := range data {
			if evType, ok := msg["ev"].(string); ok {
				if handlers, ok := c.handlers[evType]; ok {
					for _, handler := range handlers {
						msgBytes, _ := json.Marshal(msg)
						handler(msgBytes)
					}
				}
			}
		}
	}
}

// 心跳检测
func (c *WebSocketClient) heartbeat() {
	ticker := time.NewTicker(30 * time.Second)
	defer ticker.Stop()

	for {
		<-ticker.C
		if !c.IsConnected() {
			return
		}

		// 发送ping消息
		c.mu.Lock()
		err := c.conn.WriteMessage(websocket.PingMessage, []byte{})
		c.mu.Unlock()

		if err != nil {
			c.logger.Printf("发送心跳消息失败: %v", err)
			c.reconnect()
			return
		}
	}
}

// 重新连接
func (c *WebSocketClient) reconnect() {
	c.mu.Lock()
	c.isAlive = false
	c.mu.Unlock()

	c.logger.Println("连接断开，5秒后尝试重连...")
	time.Sleep(5 * time.Second)

	for i := 0; i < 5; i++ {
		err := c.Connect()
		if err == nil {
			return
		}
		c.logger.Printf("重连失败，%d秒后重试...", (i+1)*5)
		time.Sleep(time.Duration(i+1) * 5 * time.Second)
	}

	c.logger.Println("重连失败，放弃重连")
}
