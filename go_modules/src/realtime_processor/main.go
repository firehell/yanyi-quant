package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"
	"time"
)

// 配置结构体
type Config struct {
	APIKey        string `json:"api_key"`
	WSHost        string `json:"ws_host"`
	RESTHost      string `json:"rest_host"`
	DBHost        string `json:"db_host"`
	DBPort        int    `json:"db_port"`
	DBUser        string `json:"db_user"`
	DBPassword    string `json:"db_password"`
	DBName        string `json:"db_name"`
	LogFile       string `json:"log_file"`
	StocksFile    string `json:"stocks_file"`
	MaxGoroutines int    `json:"max_goroutines"`
}

// 初始化配置
func initConfig(configPath string) (*Config, error) {
	var config Config

	// 如果配置文件路径为空，使用默认配置
	if configPath == "" {
		config = Config{
			APIKey:        "1c8e3e1a-7f13-4a88-a436-62a01886e16f",
			WSHost:        "wss://socket.polygon.io/stocks",
			RESTHost:      "https://api.polygon.io",
			DBHost:        "localhost",
			DBPort:        3306,
			DBUser:        "root",
			DBPassword:    "password", // 修改为实际密码
			DBName:        "yanyi_quant",
			LogFile:       "logs/realtime_processor.log",
			StocksFile:    "config/watchlist.json",
			MaxGoroutines: 100,
		}
	} else {
		// 读取配置文件
		configFile, err := os.ReadFile(configPath)
		if err != nil {
			return nil, fmt.Errorf("读取配置文件失败: %v", err)
		}

		// 解析JSON配置
		err = json.Unmarshal(configFile, &config)
		if err != nil {
			return nil, fmt.Errorf("解析配置文件失败: %v", err)
		}
	}

	return &config, nil
}

// 初始化日志
func initLogger(logFile string) (*log.Logger, error) {
	// 确保日志目录存在
	dir := logFile[:len(logFile)-len("/realtime_processor.log")]
	if _, err := os.Stat(dir); os.IsNotExist(err) {
		err = os.MkdirAll(dir, 0755)
		if err != nil {
			return nil, fmt.Errorf("创建日志目录失败: %v", err)
		}
	}

	// 打开日志文件
	file, err := os.OpenFile(logFile, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		return nil, fmt.Errorf("打开日志文件失败: %v", err)
	}

	// 创建日志记录器
	logger := log.New(file, "", log.LstdFlags|log.Lshortfile)
	return logger, nil
}

// 读取关注股票列表
func readStockList(filePath string) ([]string, error) {
	// 如果文件不存在，返回默认股票列表
	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		return []string{"AAPL", "MSFT", "AMZN", "GOOGL", "FB"}, nil
	}

	// 读取文件
	file, err := os.ReadFile(filePath)
	if err != nil {
		return nil, fmt.Errorf("读取股票列表文件失败: %v", err)
	}

	// 解析JSON
	var stocks []string
	err = json.Unmarshal(file, &stocks)
	if err != nil {
		return nil, fmt.Errorf("解析股票列表文件失败: %v", err)
	}

	return stocks, nil
}

func main() {
	// 解析命令行参数
	configPath := flag.String("config", "", "配置文件路径")
	flag.Parse()

	// 初始化配置
	config, err := initConfig(*configPath)
	if err != nil {
		log.Fatalf("初始化配置失败: %v", err)
	}

	// 初始化日志
	logger, err := initLogger(config.LogFile)
	if err != nil {
		log.Fatalf("初始化日志失败: %v", err)
	}
	logger.Println("实时数据处理模块启动")

	// 读取关注股票列表
	stocks, err := readStockList(config.StocksFile)
	if err != nil {
		logger.Printf("读取股票列表失败: %v，使用默认列表", err)
		stocks = []string{"AAPL", "MSFT", "AMZN", "GOOGL", "FB"}
	}
	logger.Printf("关注股票: %v", stocks)

	// 创建数据聚合器
	aggregator, err := NewDataAggregator(config, logger)
	if err != nil {
		logger.Fatalf("创建数据聚合器失败: %v", err)
	}
	defer aggregator.Close()

	// 启动数据保存例程
	aggregator.StartSavingRoutine(1 * time.Minute)

	// 创建WebSocket客户端
	wsClient := NewWebSocketClient(config.WSHost, config.APIKey, logger)

	// 添加处理器
	wsClient.AddHandler("T", aggregator.ProcessTrade)
	wsClient.AddHandler("AM", aggregator.ProcessAggregate)

	// 连接WebSocket
	err = wsClient.Connect()
	if err != nil {
		logger.Fatalf("连接WebSocket失败: %v", err)
	}

	// 订阅股票数据
	channels := []string{"T", "AM"}
	err = wsClient.Subscribe(stocks, channels)
	if err != nil {
		logger.Fatalf("订阅股票数据失败: %v", err)
	}

	// 处理程序退出信号
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	// 等待退出信号
	go func() {
		sig := <-sigChan
		logger.Printf("接收到信号: %v, 准备退出...", sig)
		wsClient.Disconnect()
		aggregator.Close()
		os.Exit(0)
	}()

	// 保持主程序运行
	logger.Println("程序正在运行，按Ctrl+C退出")
	select {} // 阻塞主程序
}

// DataProcessor 数据处理器
type DataProcessor struct {
	config *Config
	logger *log.Logger
	// TODO: 添加WebSocket客户端、数据库连接等
}

// NewDataProcessor 创建新的数据处理器
func NewDataProcessor(config *Config, logger *log.Logger) *DataProcessor {
	return &DataProcessor{
		config: config,
		logger: logger,
	}
}

// Start 启动数据处理
func (p *DataProcessor) Start() error {
	p.logger.Println("数据处理器启动")
	// TODO: 实现WebSocket连接、数据处理等逻辑
	return nil
}
