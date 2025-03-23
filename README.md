# 美股日内交易辅助系统 (Yanyi-Quant)

基于 Polygon 数据的美股日内交易辅助系统，结合技术分析和 AI 模型，辅助进行日内交易决策。

## 项目介绍

本系统利用历史和实时美股数据，结合技术分析和 AI 模型，辅助用户进行日内交易决策，筛选潜力股票，提高交易胜率和盈利能力。系统不直接进行自动交易，而是为用户提供买卖点建议、股票筛选等辅助信息，最终决策权仍由用户掌握。

## 系统架构

* **编程语言:** Python (数据分析、AI模型、策略逻辑) + Go (高性能数据处理、实时数据、模拟交易)
* **数据库:** MySQL
* **数据库管理工具:** Navicat
* **AI框架:** TensorFlow/PyTorch + scikit-learn

## 功能模块

1. **数据模块**
   - 历史数据导入和清洗
   - 实时数据接口对接（Polygon）
   - 数据访问层
   
2. **技术分析模块**
   - 常用技术指标计算
   - 自定义指标接口
   - 基于指标的信号生成
   - K线形态识别
   - 图表形态识别
   
3. **AI 模型模块**
   - 特征工程
   - 模型选择与训练
   - 模型预测
   - 股票筛选
   
4. **交易执行模块**
   - 模拟交易环境
   - 模拟订单管理
   - 风险控制
   - 交易记录与报告

5. **用户界面模块**
   - 实时行情展示
   - 技术指标展示
   - 交易信号展示
   - 账户信息展示
   - 自定义工作区

## 开发进度

### 阶段1：数据准备与基础环境搭建
- [x] 数据库环境搭建（MySQL）
- [x] 历史数据导入
- [x] 数据清洗模块
- [x] Polygon WebSocket连接
- [x] 实时数据处理模块（Go）
- [x] 数据访问层（Python/Go）

### 阶段2：技术分析模块开发
- [ ] 常用技术指标计算
- [ ] 自定义指标接口
- [ ] 基于指标的信号生成
- [ ] K线形态识别
- [ ] 图表形态识别
- [ ] 信号组合与过滤

### 阶段3：AI模型模块开发
- [ ] 特征工程
- [ ] 模型选择与训练
- [ ] 模型预测模块
- [ ] 股票筛选功能

### 阶段4：交易执行模块开发
- [ ] 模拟交易环境搭建
- [ ] 模拟订单管理
- [ ] 模拟风险控制
- [ ] 交易记录与报告生成
- [ ] 交易信号推送

### 阶段5：用户界面开发
- [ ] UI 原型设计
- [ ] 实时行情展示
- [ ] 技术指标展示
- [ ] 交易信号展示与管理
- [ ] 模拟账户信息展示
- [ ] 自定义工作区功能

## 安装指南

### 环境要求
- Python 3.8+
- Go 1.16+
- MySQL 8.0+

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/yanyi-quant.git
cd yanyi-quant
```

2. 安装Python依赖
```bash
pip install -r requirements.txt
```

3. 编译Go模块
```bash
cd go_modules/src/realtime_processor
go mod init realtime_processor
go mod tidy
go build
```

4. 配置数据库
```sql
-- 创建数据库
CREATE DATABASE yanyi_quant;

-- 创建数据表
USE yanyi_quant;
CREATE TABLE stock_minute_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    open DECIMAL(10, 4) NOT NULL,
    high DECIMAL(10, 4) NOT NULL,
    low DECIMAL(10, 4) NOT NULL,
    close DECIMAL(10, 4) NOT NULL,
    volume BIGINT NOT NULL,
    vwap DECIMAL(10, 4),
    INDEX (symbol, date, time)
);

CREATE TABLE stock_minute_data_cleaned (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    open DECIMAL(10, 4) NOT NULL,
    high DECIMAL(10, 4) NOT NULL,
    low DECIMAL(10, 4) NOT NULL,
    close DECIMAL(10, 4) NOT NULL,
    volume BIGINT NOT NULL,
    vwap DECIMAL(10, 4),
    INDEX (symbol, date, time)
);
```

5. 修改配置
修改 `app/config/config.py` 中的数据库连接信息和Polygon API密钥。

## 使用方法

### 数据清洗
```bash
python -m app.main --clean --symbol AAPL --start-date 2023-01-01 --end-date 2023-01-31
```

### 启动实时数据处理
```bash
python -m app.main --realtime
```

### 启动Go实时数据处理模块
```bash
cd go_modules/src/realtime_processor
./realtime_processor
```

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交变更 (`git commit -m 'Add some amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 风险提示

*   **市场风险:** 量化交易并不能保证盈利，市场波动可能导致亏损。
*   **模型风险:** AI 模型的预测并非 100% 准确，可能出现误判。
*   **技术风险:** 系统故障、网络中断等可能导致交易失败或延迟。
*   **监管风险:** 量化交易可能受到监管政策的影响。
