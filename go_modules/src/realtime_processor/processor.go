package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"strconv"
	"sync"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

// StockData 股票数据结构
type StockData struct {
	Symbol    string
	Timestamp time.Time
	Open      float64
	High      float64
	Low       float64
	Close     float64
	Volume    int64
	VWAP      float64
}

// TradeMessage 交易消息结构
type TradeMessage struct {
	EventType  string  `json:"ev"`
	Symbol     string  `json:"sym"`
	Exchange   int     `json:"x"`
	Price      float64 `json:"p"`
	Size       int64   `json:"s"`
	Timestamp  int64   `json:"t"`
	Conditions []int   `json:"c"`
}

// AggregateMessage 聚合消息结构
type AggregateMessage struct {
	EventType string  `json:"ev"`
	Symbol    string  `json:"sym"`
	Open      float64 `json:"o"`
	High      float64 `json:"h"`
	Low       float64 `json:"l"`
	Close     float64 `json:"c"`
	Volume    int64   `json:"v"`
	VWAP      float64 `json:"vw"`
	Timestamp int64   `json:"t"`
	Start     int64   `json:"s"`
	End       int64   `json:"e"`
}

// DataAggregator 数据聚合器
type DataAggregator struct {
	mu         sync.Mutex
	data       map[string]*StockData
	db         *sql.DB
	logger     *log.Logger
	insertStmt *sql.Stmt
	config     *Config
}

// NewDataAggregator 创建新的数据聚合器
func NewDataAggregator(config *Config, logger *log.Logger) (*DataAggregator, error) {
	// 连接数据库
	dsn := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8mb4&parseTime=true",
		config.DBUser, config.DBPassword, config.DBHost, config.DBPort, config.DBName)
	db, err := sql.Open("mysql", dsn)
	if err != nil {
		return nil, fmt.Errorf("连接数据库失败: %v", err)
	}

	// 测试数据库连接
	err = db.Ping()
	if err != nil {
		return nil, fmt.Errorf("测试数据库连接失败: %v", err)
	}

	// 准备SQL语句
	insertSQL := `
	INSERT INTO stock_minute_data 
	(symbol, date, time, open, high, low, close, volume, vwap) 
	VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
	`
	stmt, err := db.Prepare(insertSQL)
	if err != nil {
		return nil, fmt.Errorf("准备SQL语句失败: %v", err)
	}

	return &DataAggregator{
		data:       make(map[string]*StockData),
		db:         db,
		logger:     logger,
		insertStmt: stmt,
		config:     config,
	}, nil
}

// ProcessTrade 处理交易消息
func (a *DataAggregator) ProcessTrade(message []byte) {
	var trade TradeMessage
	err := json.Unmarshal(message, &trade)
	if err != nil {
		a.logger.Printf("解析交易消息失败: %v", err)
		return
	}

	// 处理时间戳（纳秒转换为时间）
	timestamp := time.Unix(0, trade.Timestamp)

	a.mu.Lock()
	defer a.mu.Unlock()

	// 获取或创建股票数据
	key := fmt.Sprintf("%s_%s", trade.Symbol, timestamp.Format("2006-01-02_15:04"))
	data, ok := a.data[key]
	if !ok {
		data = &StockData{
			Symbol:    trade.Symbol,
			Timestamp: timestamp.Truncate(time.Minute),
			Open:      trade.Price,
			High:      trade.Price,
			Low:       trade.Price,
			Close:     trade.Price,
			Volume:    trade.Size,
			VWAP:      trade.Price,
		}
		a.data[key] = data
	} else {
		// 更新数据
		if trade.Price > data.High {
			data.High = trade.Price
		}
		if trade.Price < data.Low {
			data.Low = trade.Price
		}
		data.Close = trade.Price
		data.Volume += trade.Size
		// VWAP 计算公式: (price1*size1 + price2*size2 + ...) / (size1 + size2 + ...)
		// 这里使用简化计算，实际应用可能需要更复杂的算法
		data.VWAP = (data.VWAP*float64(data.Volume-trade.Size) + trade.Price*float64(trade.Size)) / float64(data.Volume)
	}
}

// ProcessAggregate 处理聚合消息
func (a *DataAggregator) ProcessAggregate(message []byte) {
	var agg AggregateMessage
	err := json.Unmarshal(message, &agg)
	if err != nil {
		a.logger.Printf("解析聚合消息失败: %v", err)
		return
	}

	// 处理时间戳（毫秒转换为时间）
	timestamp := time.Unix(0, agg.Timestamp*1000000)

	a.mu.Lock()
	defer a.mu.Unlock()

	// 直接使用聚合数据
	key := fmt.Sprintf("%s_%s", agg.Symbol, timestamp.Format("2006-01-02_15:04"))
	a.data[key] = &StockData{
		Symbol:    agg.Symbol,
		Timestamp: timestamp.Truncate(time.Minute),
		Open:      agg.Open,
		High:      agg.High,
		Low:       agg.Low,
		Close:     agg.Close,
		Volume:    agg.Volume,
		VWAP:      agg.VWAP,
	}
}

// SaveData 保存数据到数据库
func (a *DataAggregator) SaveData() {
	a.mu.Lock()
	defer a.mu.Unlock()

	if len(a.data) == 0 {
		return
	}

	// 开始事务
	tx, err := a.db.Begin()
	if err != nil {
		a.logger.Printf("开始事务失败: %v", err)
		return
	}

	// 准备语句
	stmt := tx.Stmt(a.insertStmt)

	// 保存数据
	saved := 0
	errors := 0
	for key, data := range a.data {
		// 提取日期和时间
		date := data.Timestamp.Format("2006-01-02")
		time := data.Timestamp.Format("15:04:05")

		// 执行插入
		_, err := stmt.Exec(
			data.Symbol,
			date,
			time,
			strconv.FormatFloat(data.Open, 'f', 4, 64),
			strconv.FormatFloat(data.High, 'f', 4, 64),
			strconv.FormatFloat(data.Low, 'f', 4, 64),
			strconv.FormatFloat(data.Close, 'f', 4, 64),
			data.Volume,
			strconv.FormatFloat(data.VWAP, 'f', 4, 64),
		)

		if err != nil {
			a.logger.Printf("插入数据失败 (%s): %v", key, err)
			errors++
		} else {
			saved++
			delete(a.data, key)
		}
	}

	// 提交事务
	err = tx.Commit()
	if err != nil {
		a.logger.Printf("提交事务失败: %v", err)
		tx.Rollback()
		return
	}

	a.logger.Printf("已保存 %d 条数据（失败 %d 条）", saved, errors)
}

// StartSavingRoutine 启动数据保存例程
func (a *DataAggregator) StartSavingRoutine(interval time.Duration) {
	ticker := time.NewTicker(interval)
	go func() {
		for range ticker.C {
			a.SaveData()
		}
	}()
}

// Close 关闭数据聚合器
func (a *DataAggregator) Close() error {
	a.SaveData()
	a.insertStmt.Close()
	return a.db.Close()
}
