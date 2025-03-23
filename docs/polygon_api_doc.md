# Polygon.io 股票 API 接口文档

## 目录
- [Polygon.io 股票 API 接口文档](#polygonio-股票-api-接口文档)
  - [目录](#目录)
  - [市场数据端点](#市场数据端点)
    - [Aggregates (Bars) - 聚合数据](#aggregates-bars---聚合数据)
      - [请求](#请求)
      - [路径参数](#路径参数)
      - [查询参数](#查询参数)
      - [响应参数](#响应参数)
    - [Grouped Daily (Bars) - 按日分组的数据](#grouped-daily-bars---按日分组的数据)
      - [描述](#描述)
      - [请求](#请求-1)
      - [路径参数](#路径参数-1)
      - [查询参数](#查询参数-1)
      - [响应参数](#响应参数-1)
      - [用途](#用途)
    - [Daily Open/Close - 每日开盘/收盘价](#daily-openclose---每日开盘收盘价)
      - [请求](#请求-2)
      - [路径参数](#路径参数-2)
      - [查询参数](#查询参数-2)
      - [响应参数](#响应参数-2)
    - [Previous Close - 前一日收盘价](#previous-close---前一日收盘价)
      - [请求](#请求-3)
      - [路径参数](#路径参数-3)
      - [查询参数](#查询参数-3)
      - [响应参数](#响应参数-3)
    - [Trades - 交易数据](#trades---交易数据)
      - [描述](#描述-1)
    - [Last Trade - 最新交易](#last-trade---最新交易)
      - [请求](#请求-4)
      - [路径参数](#路径参数-4)
      - [响应参数](#响应参数-4)
    - [Quotes (NBBO) - 报价数据](#quotes-nbbo---报价数据)
      - [描述](#描述-2)
    - [Last Quote - 最新报价](#last-quote---最新报价)
      - [描述](#描述-3)
  - [快照数据](#快照数据)
    - [All Tickers - 所有股票](#all-tickers---所有股票)
      - [描述](#描述-4)
    - [Gainers/Losers - 涨幅最大/跌幅最大的股票](#gainerslosers---涨幅最大跌幅最大的股票)
      - [描述](#描述-5)
    - [Ticker - 特定股票快照](#ticker---特定股票快照)
      - [请求](#请求-5)
      - [路径参数](#路径参数-5)
      - [响应参数](#响应参数-5)
    - [Universal Snapshot - 通用快照](#universal-snapshot---通用快照)
      - [请求](#请求-6)
      - [描述](#描述-6)
      - [查询参数](#查询参数-4)
      - [响应参数](#响应参数-6)
      - [用途](#用途-1)
      - [市场状态](#市场状态)
    - [Full Market Snapshot (整个市场快照)](#full-market-snapshot-整个市场快照)
      - [请求](#请求-7)
      - [查询参数](#查询参数-5)
      - [响应参数](#响应参数-7)
      - [用途](#用途-2)
      - [数据刷新](#数据刷新)
    - [Top Market Movers - 市场表现最好的股票](#top-market-movers---市场表现最好的股票)
      - [描述](#描述-7)
      - [请求](#请求-8)
      - [路径参数](#路径参数-6)
      - [查询参数](#查询参数-6)
      - [响应参数](#响应参数-8)
      - [数据筛选](#数据筛选)
      - [用途](#用途-3)
      - [数据刷新](#数据刷新-1)
  - [技术指标](#技术指标)
    - [Simple Moving Average (SMA) - 简单移动平均线](#simple-moving-average-sma---简单移动平均线)
      - [请求](#请求-9)
      - [路径参数](#路径参数-7)
      - [查询参数](#查询参数-7)
      - [响应参数](#响应参数-9)
    - [Exponential Moving Average (EMA) - 指数移动平均线](#exponential-moving-average-ema---指数移动平均线)
      - [描述](#描述-8)
    - [Moving Average Convergence/Divergence (MACD) - 移动平均线收敛/发散](#moving-average-convergencedivergence-macd---移动平均线收敛发散)
      - [请求](#请求-10)
      - [附加查询参数（除了标准技术指标参数外）](#附加查询参数除了标准技术指标参数外)
      - [响应参数](#响应参数-10)
    - [Relative Strength Index (RSI) - 相对强弱指标](#relative-strength-index-rsi---相对强弱指标)
      - [请求](#请求-11)
      - [响应参数](#响应参数-11)
  - [参考数据端点](#参考数据端点)
    - [Tickers - 股票代码](#tickers---股票代码)
      - [请求](#请求-12)
      - [查询参数](#查询参数-8)
      - [响应参数](#响应参数-12)
    - [Ticker Details v3 - 股票详情](#ticker-details-v3---股票详情)
      - [请求](#请求-13)
      - [路径参数](#路径参数-8)
      - [查询参数](#查询参数-9)
      - [响应参数](#响应参数-13)
  - [认证](#认证)
  - [返回格式](#返回格式)
  - [市场运营](#市场运营)
    - [Exchanges - 交易所](#exchanges---交易所)
      - [请求](#请求-14)
      - [描述](#描述-9)
      - [查询参数](#查询参数-10)
      - [响应参数](#响应参数-14)
      - [用途](#用途-4)
  - [市场运营](#市场运营-1)
    - [Exchanges - 交易所](#exchanges---交易所-1)
      - [请求](#请求-15)
      - [描述](#描述-10)
      - [查询参数](#查询参数-11)
      - [响应参数](#响应参数-15)
      - [用途](#用途-5)
    - [Market Holidays - 市场假期](#market-holidays---市场假期)
      - [请求](#请求-16)
      - [描述](#描述-11)
      - [响应参数](#响应参数-16)
      - [用途](#用途-6)
    - [Market Status - 市场状态](#market-status---市场状态)
      - [请求](#请求-17)
      - [描述](#描述-12)
      - [响应参数](#响应参数-17)
      - [用途](#用途-7)
    - [Condition Codes - 条件代码](#condition-codes---条件代码)
      - [请求](#请求-18)
      - [描述](#描述-13)
      - [查询参数](#查询参数-12)
      - [响应参数](#响应参数-18)
      - [用途](#用途-8)
  - [公司行动 - Corporate Actions](#公司行动---corporate-actions)
    - [首次公开发行 (IPOs)](#首次公开发行-ipos)
      - [请求](#请求-19)
      - [描述](#描述-14)
      - [查询参数](#查询参数-13)
      - [响应参数](#响应参数-19)
      - [用途](#用途-9)
  - [股票拆分 (Splits)](#股票拆分-splits)
    - [请求](#请求-20)
    - [描述](#描述-15)
    - [查询参数](#查询参数-14)
    - [响应参数](#响应参数-20)
    - [用途](#用途-10)
  - [股息 (Dividends)](#股息-dividends)
    - [请求](#请求-21)
    - [描述](#描述-16)
    - [查询参数](#查询参数-15)
    - [响应参数](#响应参数-21)
    - [用途](#用途-11)

## 市场数据端点

### Aggregates (Bars) - 聚合数据

#### 请求
```
GET /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}
```

#### 路径参数
- `stocksTicker` (必需): 股票代码，例如 AAPL 代表苹果公司
- `multiplier` (必需): 时间跨度的乘数
- `timespan` (必需): 时间窗口大小，可选值: second, minute, hour, day, week, month, quarter, year
- `from` (必需): 聚合时间窗口的开始。格式为 YYYY-MM-DD 或毫秒时间戳
- `to` (必需): 聚合时间窗口的结束。格式为 YYYY-MM-DD 或毫秒时间戳

#### 查询参数
- `adjusted` (可选): 结果是否针对股票拆分进行调整，默认为 true
- `sort` (可选): 按时间戳排序，asc (升序), desc (降序)
- `limit` (可选): 限制用于创建聚合结果的基础聚合数量，最大 50000，默认 5000

#### 响应参数
```json
{
  "ticker": "AAPL",         // 交易的股票代码
  "adjusted": true,         // 是否针对股票拆分进行调整
  "queryCount": 10,         // 用于生成响应的聚合数量
  "request_id": "abc123",   // 服务器分配的请求ID
  "resultsCount": 5,        // 此请求的结果总数
  "status": "OK",           // 此请求响应的状态
  "results": [              // 结果数组
    {
      "c": 156.78,          // 收盘价
      "h": 158.45,          // 最高价
      "l": 154.32,          // 最低价
      "n": 1000,            // 聚合窗口中的交易数量
      "o": 155.23,          // 开盘价
      "t": 1617302400000,   // 聚合窗口开始的Unix毫秒时间戳
      "v": 10345678,        // 交易量
      "vw": 156.25          // 成交量加权平均价
    }
  ]
}
```

### Grouped Daily (Bars) - 按日分组的数据

#### 描述
获取市场上每个股票的每日聚合，返回每个股票的开盘价、最高价、最低价和收盘价（OHLC）。

#### 请求
```
GET /v2/aggs/grouped/locale/us/market/stocks/{date}
```

#### 路径参数
- `date` (必需): 聚合窗口的开始日期。

#### 查询参数
- `adjusted` (可选): 结果是否针对股票拆分进行调整，默认为 true。
- `include_otc` (可选): 是否在响应中包含场外交易（OTC）证券，默认为 false。

#### 响应参数
```json
{
  "adjusted": true,         // 是否针对股票拆分进行调整
  "queryCount": 10,         // 用于生成响应的聚合数量
  "request_id": "abc123",   // 服务器分配的请求ID
  "resultsCount": 5000,     // 此请求的结果总数
  "status": "OK",           // 此请求响应的状态
  "results": [              // 结果数组
    {
      "T": "AAPL",          // 交易的股票代码
      "c": 156.78,          // 收盘价
      "h": 158.45,          // 最高价
      "l": 154.32,          // 最低价
      "n": 1000,            // 聚合窗口中的交易数量(可选)
      "o": 155.23,          // 开盘价
      "otc": false,         // 是否为OTC股票(如果为false，则省略该字段)
      "t": 1617302400000,   // 聚合窗口结束的Unix毫秒时间戳
      "v": 10345678,        // 交易量
      "vw": 156.25          // 成交量加权平均价(可选)
    }
    // 更多结果...
  ]
}
```

#### 用途
此端点适用于：
- 市场概览
- 批量数据处理
- 历史研究
- 投资组合比较

### Daily Open/Close - 每日开盘/收盘价

#### 请求
```
GET /v1/open-close/{stocksTicker}/{date}
```

#### 路径参数
- `stocksTicker` (必需): 股票代码，例如 AAPL 代表苹果公司
- `date` (必需): 请求的开盘/收盘日期，格式为 YYYY-MM-DD

#### 查询参数
- `adjusted` (可选): 结果是否针对股票拆分进行调整，默认为 true

#### 响应参数
```json
{
  "afterHours": 322.1,      // 盘后交易收盘价
  "close": 325.12,          // 收盘价
  "from": "2023-01-09",     // 请求的日期
  "high": 326.2,            // 最高价
  "low": 322.3,             // 最低价
  "open": 324.66,           // 开盘价
  "preMarket": 324.5,       // 盘前交易开盘价
  "status": "OK",           // 此请求响应的状态
  "symbol": "AAPL",         // 交易的股票代码
  "volume": 26122646        // 交易量
}
```

### Previous Close - 前一日收盘价

#### 请求
```
GET /v2/aggs/ticker/{stocksTicker}/prev
```

#### 路径参数
- `stocksTicker` (必需): 股票代码，例如 AAPL 代表苹果公司

#### 查询参数
- `adjusted` (可选): 结果是否针对股票拆分进行调整，默认为 true

#### 响应参数
```json
{
  "ticker": "AAPL",         // 交易的股票代码
  "adjusted": true,         // 是否针对股票拆分进行调整
  "queryCount": 1,          // 用于生成响应的聚合数量
  "request_id": "abc123",   // 服务器分配的请求ID
  "resultsCount": 1,        // 此请求的结果总数
  "status": "OK",           // 此请求响应的状态
  "results": [              // 结果数组
    {
      "c": 156.78,          // 收盘价
      "h": 158.45,          // 最高价
      "l": 154.32,          // 最低价
      "n": 1000,            // 聚合窗口中的交易数量
      "o": 155.23,          // 开盘价
      "t": 1617302400000,   // 聚合窗口开始的Unix毫秒时间戳
      "v": 10345678,        // 交易量
      "vw": 156.25          // 成交量加权平均价
    }
  ]
}
```

### Trades - 交易数据

#### 描述
获取特定股票的历史交易数据。

### Last Trade - 最新交易

#### 请求
```
GET /v2/last/trade/{stocksTicker}
```

#### 路径参数
- `stocksTicker` (必需): 股票代码，例如 AAPL 代表苹果公司

#### 响应参数
```json
{
  "request_id": "abc123",   // 服务器分配的请求ID
  "results": {              // 包含请求的交易数据
    "T": "AAPL",            // 交易的股票代码
    "c": [12, 41],          // 条件代码列表
    "e": 1,                 // 交易更正指示器
    "f": 1517562000015577,  // TRF(交易报告设施)接收此消息的纳秒精度Unix时间戳
    "i": "12345",           // 交易ID，唯一标识一笔交易
    "p": 171.55,            // 交易价格，每股的实际美元价值
    "q": 1063,              // 序列号，表示消息事件发生的顺序
    "r": 1,                 // 交易发生的交易报告设施的ID
    "s": 100,               // 交易的规模（也称为交易量）
    "t": 1517562000016036,  // SIP接收此消息的纳秒精度Unix时间戳
    "x": 11,                // 交易所ID
    "y": 1517562000015577,  // 交易实际生成的纳秒精度Unix时间戳
    "z": 3                  // 定义股票在哪个交易所上市的磁带
  },
  "status": "OK"            // 此请求响应的状态
}
```

### Quotes (NBBO) - 报价数据

#### 描述
获取特定股票的历史报价数据。

### Last Quote - 最新报价

#### 描述
获取特定股票的最新可用报价。

## 快照数据

### All Tickers - 所有股票

#### 描述
获取所有交易股票的最新市场数据。

### Gainers/Losers - 涨幅最大/跌幅最大的股票

#### 描述
获取当天涨幅最大和跌幅最大的股票。

### Ticker - 特定股票快照

#### 请求
```
GET /v2/snapshot/locale/us/markets/stocks/tickers/{stocksTicker}
```

#### 路径参数
- `stocksTicker` (必需): 股票代码，例如 AAPL 代表苹果公司

#### 响应参数
```json
{
  "status": "OK",           // 此请求响应的状态
  "request_id": "abc123",   // 服务器分配的请求ID
  "ticker": {               // 股票信息
    "day": {                // 此股票最近的每日K线
      "c": 156.78,          // 收盘价
      "h": 158.45,          // 最高价
      "l": 154.32,          // 最低价
      "o": 155.23,          // 开盘价
      "v": 10345678,        // 交易量
      "vw": 156.25          // 成交量加权平均价
    },
    "lastQuote": {          // 此股票最近的报价
      "P": 156.85,          // 卖价
      "S": 11,              // 卖出数量（以手为单位）
      "p": 156.75,          // 买价
      "s": 25,              // 买入数量（以手为单位）
      "t": 1617302400000    // SIP接收此消息的纳秒精度Unix时间戳
    },
    "lastTrade": {          // 此股票最近的交易
      "c": [63],            // 交易条件
      "i": "12345",         // 交易ID
      "p": 156.78,          // 交易价格
      "s": 536,             // 交易数量
      "t": 1617302400000,   // 交易时间戳
      "x": 4                // 交易所ID
    },
    "min": {                // 最近的分钟K线
      "av": 10345678,       // 累计成交量
      "c": 156.78,          // 收盘价
      "h": 156.85,          // 最高价
      "l": 156.65,          // 最低价
      "n": 5,               // 交易次数
      "o": 156.7,           // 开盘价
      "t": 1617302400000,   // 时间戳
      "v": 6108,            // 成交量
      "vw": 156.75          // 成交量加权平均价
    },
    "prevDay": {            // 前一天的K线
      "c": 155.23,          // 收盘价
      "h": 157.35,          // 最高价
      "l": 154.21,          // 最低价
      "o": 156.34,          // 开盘价
      "v": 15680970,        // 成交量
      "vw": 155.85          // 成交量加权平均价
    },
    "ticker": "AAPL",       // 股票代码
    "todaysChange": 1.55,   // 今日变化值
    "todaysChangePerc": 1.00, // 今日变化百分比
    "updated": 1617302400000 // 最后更新时间戳
  }
}
```

### Universal Snapshot - 通用快照

#### 请求
```
GET /v3/snapshot
```

#### 描述
在单个请求中检索包括股票、期权、外汇和加密货币在内的多个资产类别的统一市场数据快照。该端点整合了来自各种来源的关键指标，如最新交易、最新报价、开盘价、最高价、最低价、收盘价和交易量，提供当前市场状况的全面视图。通过将来自多个市场的数据汇总到一个响应中，用户可以高效地监控、比较和处理跨越多个市场和资产类型的信息。

#### 查询参数
- `ticker` (可选): 词典顺序搜索一系列股票代码
- `type` (可选): 按资产类型查询，可选值: stocks, options, fx, crypto, indices
- `order` (可选): 基于 `sort` 字段的排序顺序，可选值: asc, desc
- `limit` (可选): 限制返回的结果数量，默认为 10，最大为 250
- `sort` (可选): 用于排序的字段

#### 响应参数
```json
{
  "next_url": "https://api.polygon.io/v3/snapshot?cursor=...", // 如果存在，此值可用于获取下一页数据
  "request_id": "abc123",   // 服务器分配的请求ID
  "results": [              // 包含请求数据的结果数组
    {
      "break_even_price": 145.5, // 期权合约盈亏平衡价格（可选，仅适用于期权）
      "details": {          // 合约详情（可选）
        // 合约详情字段
      },
      "error": "错误信息",  // 查找此股票时的错误（可选）
      "fmv": 156.80,        // 公平市场价值（仅商业计划可用）
      "greeks": {           // 期权希腊字母（可选，仅适用于期权）
        // 希腊字母字段
      },
      "implied_volatility": 0.28, // 基于期权当前价格的标的资产波动率预测（可选，仅适用于期权）
      "last_quote": {       // 此合约的最新报价（仅当您的计划包含报价时返回）
        // 最新报价字段
      },
      "last_trade": {       // 此合约的最新交易（仅当您的计划包含交易时返回）
        // 最新交易字段
      },
      "market_status": "open", // 交易此股票的市场状态
      "message": "消息内容", // 查找此股票时的错误消息（可选）
      "name": "Apple Inc.", // 此合约的名称（可选）
      "open_interest": 1500, // 上一个交易日结束时持有的此合约数量（可选，仅适用于期权）
      "session": {          // 全面的交易会话指标
        // 交易会话数据字段
      },
      "ticker": "AAPL",     // 资产的股票代码
      "type": "stocks",     // 此股票的资产类别（可选）
      "underlying_asset": { // 此期权合约的标的股票信息（可选，仅适用于期权）
        // 标的资产字段
      },
      "value": 3850.25      // 指数值（可选，仅适用于指数）
    }
    // 更多结果...
  ],
  "status": "OK"            // 此请求响应的状态
}
```

#### 用途
此端点适用于：
- 跨市场分析
- 多元化投资组合监控
- 全球市场洞察
- 多资产交易策略

#### 市场状态
股票、期权、加密货币和外汇快照的可能市场状态值有：`open`（开盘）、`closed`（收盘）、`early_trading`（早盘交易）或 `late_trading`（晚盘交易）。

指数快照的可能市场状态值有：`regular_trading`（常规交易）、`closed`（收盘）、`early_trading`（早盘交易）和 `late_trading`（晚盘交易）。

参考链接：[Polygon.io Unified Snapshot](https://polygon.io/docs/rest/stocks/snapshots/unified-snapshot)

### Full Market Snapshot (整个市场快照)

这个API端点可以在"快照数据"部分下的"All Tickers"小节中进行补充，它提供了整个美国股票市场的综合性快照。

#### 请求
```
GET /v2/snapshot/locale/us/markets/stocks/tickers
```

#### 查询参数
- `tickers` (可选): 逗号分隔的股票代码列表，区分大小写。例如：AAPL,TSLA,GOOG。空字符串默认查询所有股票。
- `include_otc` (可选): 是否在响应中包含场外交易（OTC）证券。默认为false（不包含OTC证券）。

#### 响应参数
```json
{
  "count": 10245,           // 此请求的结果总数
  "status": "OK",           // 此请求响应的状态
  "tickers": [              // 股票数组
    {
      "day": {              // 此股票最近的每日K线
        "c": 156.78,        // 收盘价
        "h": 158.45,        // 最高价
        "l": 154.32,        // 最低价
        "o": 155.23,        // 开盘价
        "v": 10345678,      // 交易量
        "vw": 156.25        // 成交量加权平均价
      },
      "fmv": 156.80,        // 公平市场价值(仅商业计划可用)
      "lastQuote": {        // 此股票最近的报价(仅当您的计划包含报价时返回)
        "P": 156.85,        // 卖价
        "S": 11,            // 卖出数量(以手为单位)
        "p": 156.75,        // 买价
        "s": 25,            // 买入数量(以手为单位)
        "t": 1617302400000  // SIP接收此消息的时间戳
      },
      "lastTrade": {        // 此股票最近的交易(仅当您的计划包含交易时返回)
        "c": [63],          // 交易条件
        "i": "12345",       // 交易ID
        "p": 156.78,        // 交易价格
        "s": 536,           // 交易数量
        "t": 1617302400000, // 交易时间戳
        "x": 4              // 交易所ID
      },
      "min": {              // 最近的分钟K线
        "av": 10345678,     // 累计成交量
        "c": 156.78,        // 收盘价
        "h": 156.85,        // 最高价
        "l": 156.65,        // 最低价
        "n": 5,             // 交易次数
        "o": 156.7,         // 开盘价
        "t": 1617302400000, // 时间戳
        "v": 6108,          // 成交量
        "vw": 156.75        // 成交量加权平均价
      },
      "prevDay": {          // 前一天的K线
        "c": 155.23,        // 收盘价
        "h": 157.35,        // 最高价
        "l": 154.21,        // 最低价
        "o": 156.34,        // 开盘价
        "v": 15680970,      // 成交量
        "vw": 155.85        // 成交量加权平均价
      },
      "ticker": "AAPL",     // 股票代码
      "todaysChange": 1.55, // 今日变化值
      "todaysChangePerc": 1.00, // 今日变化百分比
      "updated": 1617302400000 // 最后更新时间戳
    }
    // 更多股票...
  ]
}
```

#### 用途
这个端点非常适合以下场景：
- 市场概览
- 批量数据处理
- 热图/仪表盘
- 自动监控

#### 数据刷新
快照数据每天在美东时间凌晨3:30清除，并在交易所报告新数据时开始重新填充，这可能早在美东时间4:00开始。

建议您将这部分内容添加到现有的markdown文档中，放在"快照数据"的"All Tickers - 所有股票"小节下，以便完善您的API文档。

参考链接：[Polygon.io Full Market Snapshot](https://polygon.io/docs/rest/stocks/snapshots/full-market-snapshot)

### Top Market Movers - 市场表现最好的股票

#### 描述
获取美国股票市场表现最好和最差的前20支股票。

#### 请求
```
GET /v2/snapshot/locale/us/markets/stocks/{direction}
```

#### 路径参数
- `direction` (必需): 获取结果的方向，可选值：
  - `gainers`: 获取涨幅最大的股票
  - `losers`: 获取跌幅最大的股票

#### 查询参数
- `include_otc` (可选): 是否在响应中包含场外交易（OTC）证券，默认为 false（不包含OTC证券）

#### 响应参数
```json
{
  "status": "OK",           // 此请求响应的状态
  "tickers": [              // 股票数组，包含前20个涨幅最大或跌幅最大的股票
    {
      "day": {              // 此股票最近的每日K线
        "c": 156.78,        // 收盘价
        "h": 158.45,        // 最高价
        "l": 154.32,        // 最低价
        "o": 155.23,        // 开盘价
        "v": 10345678,      // 交易量
        "vw": 156.25        // 成交量加权平均价
      },
      "fmv": 156.80,        // 公平市场价值(仅商业计划可用)
      "lastQuote": {        // 此股票最近的报价(仅当您的计划包含报价时返回)
        "P": 156.85,        // 卖价
        "S": 11,            // 卖出数量(以手为单位)
        "p": 156.75,        // 买价
        "s": 25,            // 买入数量(以手为单位)
        "t": 1617302400000  // SIP接收此消息的时间戳
      },
      "lastTrade": {        // 此股票最近的交易(仅当您的计划包含交易时返回)
        "c": [63],          // 交易条件
        "i": "12345",       // 交易ID
        "p": 156.78,        // 交易价格
        "s": 536,           // 交易数量
        "t": 1617302400000, // 交易时间戳
        "x": 4              // 交易所ID
      },
      "min": {              // 最近的分钟K线
        "av": 10345678,     // 累计成交量
        "c": 156.78,        // 收盘价
        "h": 156.85,        // 最高价
        "l": 156.65,        // 最低价
        "n": 5,             // 交易次数
        "o": 156.7,         // 开盘价
        "t": 1617302400000, // 时间戳
        "v": 6108,          // 成交量
        "vw": 156.75        // 成交量加权平均价
      },
      "prevDay": {          // 前一天的K线
        "c": 155.23,        // 收盘价
        "h": 157.35,        // 最高价
        "l": 154.21,        // 最低价
        "o": 156.34,        // 开盘价
        "v": 15680970,      // 成交量
        "vw": 155.85        // 成交量加权平均价
      },
      "ticker": "AAPL",     // 股票代码
      "todaysChange": 15.55, // 今日变化值
      "todaysChangePerc": 10.0, // 今日变化百分比
      "updated": 1617302400000 // 最后更新时间戳
    }
    // 更多股票...（总共20个）
  ]
}
```

#### 数据筛选
为确保获得有意义的见解，仅包含最低交易量为10,000的股票。

#### 用途
此端点适用于：
- 市场异动识别
- 交易策略
- 市场情绪分析
- 投资组合调整

#### 数据刷新
快照数据每天在美东时间凌晨3:30清除，并在交易所报告新数据时开始重新填充，这可能早在美东时间4:00开始。通过关注这些市场异动，用户可以快速识别重要的价格变化并监控不断变化的市场动态。

参考链接：[Polygon.io Top Market Movers](https://polygon.io/docs/rest/stocks/snapshots/top-market-movers)

## 技术指标

### Simple Moving Average (SMA) - 简单移动平均线

#### 请求
```
GET /v1/indicators/sma/{stockTicker}
```

#### 路径参数
- `stockTicker` (必需): 获取SMA数据的股票代码，例如 AAPL 代表苹果公司

#### 查询参数
- `timestamp` (可选): 按时间戳查询，YYYY-MM-DD格式或毫秒时间戳
- `timespan` (可选): 聚合时间窗口的大小，可选值: minute, hour, day, week, month, quarter, year
- `adjusted` (可选): 用于计算SMA的聚合是否针对股票拆分进行调整，默认为 true
- `window` (可选): 用于计算SMA的窗口大小
- `series_type` (可选): 用于计算SMA的价格类型，可选值: open, high, low, close，默认为 close
- `expand_underlying` (可选): 是否在响应中包含用于计算此指标的聚合，可选值: true, false
- `order` (可选): 返回结果的顺序，按时间戳排序，可选值: asc, desc
- `limit` (可选): 限制返回的结果数量，默认为 10，最大为 5000

#### 响应参数
```json
{
  "next_url": "https://api.polygon.io/v1/indicators/sma/AAPL?cursor=...",  // 用于获取下一页数据的URL
  "request_id": "abc123",   // 服务器分配的请求ID
  "results": {              // 结果对象
    "underlying": {         // 底层数据
      "url": "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2003-01-01/2022-07-25" // 用于请求底层聚合的URL
    },
    "values": [             // 值数组
      {
        "timestamp": 1517562000016, // 用于此计算的最后一个聚合的Unix毫秒时间戳
        "value": 140.139     // 此周期的指标值
      }
    ]
  },
  "status": "OK"            // 此请求响应的状态
}
```

### Exponential Moving Average (EMA) - 指数移动平均线

#### 描述
类似于SMA，但对最近数据赋予更大的权重，因为它被视为更相关或更重要。EMA的响应对象与SMA的响应对象一致。

### Moving Average Convergence/Divergence (MACD) - 移动平均线收敛/发散

#### 请求
```
GET /v1/indicators/macd/{stockTicker}
```

#### 附加查询参数（除了标准技术指标参数外）
- `short_window`: 用于计算短期EMA的窗口大小
- `long_window`: 用于计算长期EMA的窗口大小
- `signal_window`: 用于计算信号线的窗口大小

#### 响应参数
```json
{
  "next_url": "https://api.polygon.io/v1/indicators/macd/AAPL?cursor=...",  // 用于获取下一页数据的URL
  "request_id": "abc123",   // 服务器分配的请求ID
  "results": {              // 结果对象
    "underlying": {         // 底层数据
      "url": "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2003-01-01/2022-07-25" // 用于请求底层聚合的URL
    },
    "values": [             // 值数组
      {
        "histogram": 38.38, // 柱状图值，表示MACD与信号线的距离
        "signal": 106.98,   // 信号线值
        "timestamp": 1517562000016, // 用于此计算的最后一个聚合的Unix毫秒时间戳
        "value": 145.36     // MACD值
      }
    ]
  },
  "status": "OK"            // 此请求响应的状态
}
```

### Relative Strength Index (RSI) - 相对强弱指标

#### 请求
```
GET /v1/indicators/rsi/{stockTicker}
```

#### 响应参数
```json
{
  "next_url": "https://api.polygon.io/v1/indicators/rsi/AAPL?cursor=...",  // 用于获取下一页数据的URL
  "request_id": "abc123",   // 服务器分配的请求ID
  "results": {              // 结果对象
    "underlying": {         // 底层数据
      "url": "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2003-01-01/2022-07-25" // 用于请求底层聚合的URL
    },
    "values": [             // 值数组
      {
        "timestamp": 1517562000016, // 用于此计算的最后一个聚合的Unix毫秒时间戳
        "value": 82.19      // RSI值，介于0和100之间
      }
    ]
  },
  "status": "OK"            // 此请求响应的状态
}
```

## 参考数据端点

### Tickers - 股票代码

#### 请求
```
GET /v3/reference/tickers
```

#### 查询参数
- `ticker` (可选): 指定股票代码，默认为空字符串，查询所有股票代码
- `type` (可选): 指定股票类型，可通过Ticker Types API找到支持的类型
- `market` (可选): 按市场类型过滤，可选值: stocks, crypto, fx, otc, indices，默认包括所有市场
- `exchange` (可选): 指定资产的主要上市交易所（ISO代码格式）
- `cusip` (可选): 指定要搜索的资产的CUSIP代码
- `cik` (可选): 指定要搜索的资产的CIK代码
- `date` (可选): 指定时间点，检索该日期可用的股票代码，默认为最近可用日期
- `search` (可选): 在股票代码和/或公司名称中搜索术语
- `active` (可选): 指定返回的股票代码在查询日期是否活跃交易，默认为 true
- `order` (可选): 基于 sort 字段的排序顺序，可选值: asc, desc
- `limit` (可选): 限制返回的结果数量，默认为 100，最大为 1000
- `sort` (可选): 用于排序的字段

#### 响应参数
```json
{
  "count": 1,              // 此请求的结果总数
  "next_url": "https://api.polygon.io/v3/reference/tickers?cursor=...",  // 用于获取下一页数据的URL
  "request_id": "abc123",   // 服务器分配的请求ID
  "results": [              // 匹配查询的股票代码数组
    {
      "active": true,       // 资产是否活跃交易
      "cik": "0001090872",  // 此股票的CIK编号
      "composite_figi": "BBG000BWQYZ5", // 此股票的复合OpenFIGI编号
      "currency_name": "usd", // 此资产交易的货币名称
      "last_updated_utc": "2021-04-25T00:00:00Z", // 信息准确到的时间
      "locale": "us",       // 资产的地区
      "market": "stocks",   // 资产的市场类型
      "name": "Agilent Technologies Inc.", // 资产名称
      "primary_exchange": "XNYS", // 资产主要上市交易所的ISO代码
      "share_class_figi": "BBG001SCTQY4", // 此股票的股份类别OpenFIGI编号
      "ticker": "A",        // 此项目交易的交易所代码
      "type": "CS"          // 资产类型
    }
  ],
  "status": "OK"            // 此请求响应的状态
}
```

### Ticker Details v3 - 股票详情

#### 请求
```
GET /v3/reference/tickers/{ticker}
```

#### 路径参数
- `ticker` (必需): 资产的股票代码

#### 查询参数
- `date` (可选): 指定时间点，获取该日期可用的股票信息

#### 响应参数
```json
{
  "count": 1,              // 此请求的结果总数
  "request_id": "abc123",   // 服务器分配的请求ID
  "results": {              // 带有详情的股票
    "active": true,         // 资产是否活跃交易
    "address": {            // 公司总部地址
      "address1": "5301 Stevens Creek Blvd",
      "address2": null,
      "city": "Santa Clara",
      "postal_code": "95051",
      "state": "CA"
    },
    // 其他详细信息...
  },
  "status": "OK"            // 此请求响应的状态
}
```

## 认证
1. 查询字符串参数: `?apiKey=YOUR_API_KEY`
2. 授权头部: `Authorization: Bearer YOUR_API_KEY`

## 返回格式
默认情况下，所有端点都返回JSON响应。具有Options Starter计划及以上的用户可以通过包含 `'Accept': 'text/csv'` 作为请求参数来请求CSV响应。

参考链接：
- [Polygon.io REST Quickstart](https://polygon.io/docs/rest/quickstart)
- [Polygon.io Stocks API Documentation](https://polygon.io/docs/stocks)

## 市场运营

### Exchanges - 交易所

#### 请求
```
GET /v3/reference/exchanges
```

#### 描述
获取已知交易所的列表，包括它们的标识符、名称、市场类型和其他相关属性。这些信息有助于映射交易所代码，了解市场覆盖范围，并将交易所详情集成到应用程序中。

#### 查询参数
- `asset_class` (可选): 按资产类别过滤，可选值: stocks, options, crypto, fx
- `locale` (可选): 按地区过滤，可选值: us, global

#### 响应参数
```json
{
  "count": 30,             // 此请求的结果总数
  "request_id": "abc123",   // 服务器分配的请求ID
  "results": [              // 结果数组
    {
      "acronym": "NYSE",    // 此交易所常用的缩写
      "asset_class": "stocks", // 资产类别标识符
      "id": 1,              // Polygon.io用于此交易所的唯一标识符
      "locale": "us",       // 地理位置标识符
      "mic": "XNYS",        // 此交易所的市场标识代码(见ISO 10383)
      "name": "New York Stock Exchange", // 交易所名称
      "operating_mic": "XNYS", // 运营此交易所的实体的MIC
      "participant_id": "N", // SIP用于表示此交易所的ID
      "type": "exchange",   // 交易所类型，可选值: exchange, TRF, SIP
      "url": "https://www.nyse.com" // 指向此交易所网站的链接(如果存在)
    }
    // 更多交易所...
  ],
  "status": "OK"            // 此请求响应的状态
}
```

#### 用途
此端点适用于：
- 数据映射
- 市场覆盖分析
- 应用程序开发(例如，显示交易所选项)
- 确保监管合规性

参考链接：[Polygon.io Exchanges](https://polygon.io/docs/rest/stocks/market-operations/exchanges)


## 市场运营

### Exchanges - 交易所

#### 请求
```
GET /v3/reference/exchanges
```

#### 描述
获取已知交易所的列表，包括它们的标识符、名称、市场类型和其他相关属性。这些信息有助于映射交易所代码，了解市场覆盖范围，并将交易所详情集成到应用程序中。

#### 查询参数
- `asset_class` (可选): 按资产类别过滤，可选值: stocks, options, crypto, fx
- `locale` (可选): 按地区过滤，可选值: us, global

#### 响应参数
```json
{
  "count": 30,             // 此请求的结果总数
  "request_id": "abc123",   // 服务器分配的请求ID
  "results": [              // 结果数组
    {
      "acronym": "NYSE",    // 此交易所常用的缩写
      "asset_class": "stocks", // 资产类别标识符
      "id": 1,              // Polygon.io用于此交易所的唯一标识符
      "locale": "us",       // 地理位置标识符
      "mic": "XNYS",        // 此交易所的市场标识代码(见ISO 10383)
      "name": "New York Stock Exchange", // 交易所名称
      "operating_mic": "XNYS", // 运营此交易所的实体的MIC
      "participant_id": "N", // SIP用于表示此交易所的ID
      "type": "exchange",   // 交易所类型，可选值: exchange, TRF, SIP
      "url": "https://www.nyse.com" // 指向此交易所网站的链接(如果存在)
    }
    // 更多交易所...
  ],
  "status": "OK"            // 此请求响应的状态
}
```

#### 用途
此端点适用于：
- 数据映射
- 市场覆盖分析
- 应用程序开发(例如，显示交易所选项)
- 确保监管合规性

参考链接：[Polygon.io Exchanges](https://polygon.io/docs/rest/stocks/market-operations/exchanges)

### Market Holidays - 市场假期

#### 请求
```
GET /v1/marketstatus/upcoming
```

#### 描述
检索即将到来的市场假期及其相应的开闭市时间。此端点仅面向未来，列出影响市场交易时间的未来假期。使用此数据来提前为交易活动和系统运营做计划。

#### 响应参数
```json
{
  "response": [             // 结果数组
    {
      "close": "13:00",     // 假期当天的市场收盘时间(如果不是全天休市)
      "date": "2023-11-24", // 假期日期
      "exchange": "NASDAQ", // 记录所针对的市场
      "name": "Thanksgiving Day", // 假期名称
      "open": "9:30",       // 假期当天的市场开盘时间(如果不是全天休市)
      "status": "early-close" // 假期当天的市场状态
    }
    // 更多假期...
  ]
}
```

#### 用途
此端点适用于：
- 交易安排调整
- 集成假期日历
- 运营规划(例如，系统维护)
- 通知用户即将到来的市场休市时间

参考链接：[Polygon.io Market Holidays](https://polygon.io/docs/rest/stocks/market-operations/market-holidays)

### Market Status - 市场状态

#### 请求
```
GET /v1/marketstatus/now
```

#### 描述
获取各个交易所和整体金融市场的当前交易状态。此端点提供实时指标，显示市场是开盘、收盘还是在盘前/盘后交易时段运营，以及当前或即将到来的交易时段的时间详情。

#### 响应参数
```json
{
  "afterHours": false,      // 市场是否处于盘后时段
  "currencies": {           // 货币市场状态
    "crypto": "open",       // 加密货币市场状态
    "fx": "open"            // 外汇市场状态
  },
  "earlyHours": false,      // 市场是否处于盘前时段
  "exchanges": {            // 交易所状态
    "nasdaq": "open",       // 纳斯达克市场状态
    "nyse": "open",         // 纽约证券交易所市场状态
    "otc": "open"           // 场外交易市场状态
  },
  "indicesGroups": {        // 指数组状态
    "cccy": "extended-hours", // Cboe流式市场指数加密货币指数交易时间状态
    "cgi": "regular-trading", // Cboe全球指数交易时间状态
    "dow_jones": "regular-trading", // 道琼斯指数交易时间状态
    "ftse_russell": "regular-trading", // 富时罗素指数交易时间状态
    "msci": "regular-trading", // 摩根士丹利资本国际指数交易时间状态
    "mstar": "regular-trading", // 晨星指数交易时间状态
    "nasdaq": "regular-trading", // 纳斯达克指数交易时间状态
    "s_and_p": "regular-trading", // 标准普尔指数交易时间状态
    "societe_generale": "regular-trading" // 法国兴业银行指数交易时间状态
  },
  "market": "open",         // 整体市场状态
  "serverTime": "2023-10-16T14:30:00Z" // 服务器当前时间，以RFC3339格式的日期时间返回
}
```

#### 用途
此端点适用于：
- 实时监控
- 算法调度
- UI更新
- 运营规划

参考链接：[Polygon.io Market Status](https://polygon.io/docs/rest/stocks/market-operations/market-status)

### Condition Codes - 条件代码

#### 请求
```
GET /v3/reference/conditions
```

#### 描述
获取来自各种上游市场数据提供商(例如，CTA、UTP、OPRA、FINRA)的交易和报价条件的统一和全面列表。每个条件都标识与市场数据相关的特殊情况，例如在常规交易时段之外发生的交易或按平均价格进行的交易，并概述这些条件如何影响高、低、开盘、收盘和成交量等指标。通过检查这些映射条件，用户可以准确解释交易和报价的上下文，应用适当的过滤，并确保聚合数据正确反映合格的交易活动。

#### 查询参数
- `asset_class` (可选): 按资产类别过滤条件，可选值: stocks, options, crypto, fx
- `data_type` (可选): 按数据类型过滤，可选值: trade, quote
- `id` (可选): 按指定ID过滤条件
- `sip` (可选): 按SIP过滤，如果条件包含该SIP的映射，则会返回该条件
- `order` (可选): 基于 `sort` 字段的排序顺序，可选值: asc, desc
- `limit` (可选): 限制返回的结果数量，默认为 10，最大为 1000
- `sort` (可选): 用于排序的字段

#### 响应参数
```json
{
  "count": 200,            // 此请求的结果总数
  "next_url": "https://api.polygon.io/v3/reference/conditions?cursor=...", // 用于获取下一页数据的URL
  "request_id": "abc123",   // 服务器分配的请求ID
  "results": [              // 结果数组
    {
      "abbreviation": "@",  // 此条件常用的缩写
      "asset_class": "stocks", // 资产类别标识符
      "data_types": ["trade"], // 此条件适用的数据类型
      "description": "Regular Sale", // 此条件语义的简短描述
      "exchange": 1,        // 映射此条件的交易所ID
      "id": 1,              // Polygon.io用于此条件的标识符，每种数据类型唯一
      "legacy": false,      // 如果为true，此条件来自SIP规范的旧版本，不再使用
      "name": "Regular Sale", // 此条件的名称
      "sip_mapping": {      // 每个SIP的符号映射
        "CTA": "blank",     // CTA的符号映射
        "OPRA": "blank",    // OPRA的符号映射
        "UTP": "blank"      // UTP的符号映射
      },
      "type": "sale_condition", // 相关条件集合的标识符
      "update_rules": {     // 聚合规则列表
        "volume": "eligible", // 此条件的成交量是否计入聚合
        "high_low": "eligible", // 此条件的价格是否计入高低价计算
        "open_close": "eligible" // 此条件的价格是否计入开盘收盘价计算
      }
    }
    // 更多条件...
  ],
  "status": "OK"            // 此请求响应的状态
}
```

#### 用途
此端点适用于：
- 数据解释
- 统一条件映射
- 过滤和分析
- 算法调整
- 合规与报告

参考链接：[Polygon.io Condition Codes](https://polygon.io/docs/rest/stocks/market-operations/condition-codes)

## 公司行动 - Corporate Actions

### 首次公开发行 (IPOs)

#### 请求
```
GET /vX/reference/ipos
```

#### 描述
获取关于首次公开发行(IPOs)的全面信息，包括即将到来和历史事件。该端点提供关键详情如发行人名称、股票代码、证券类型、IPO日期、发行股份数量、预期价格范围、最终发行价格和募资规模等。用户可以按IPO状态(如待定、新上市、传闻、历史)进行筛选，以便有针对性地进行研究和制定投资决策。

#### 查询参数
- `ticker` (可选): 指定区分大小写的股票代码，例如 AAPL 代表苹果公司
- `us_code` (可选): 指定北美金融证券的唯一九位字母数字代码，用于促进交易的清算和结算
- `isin` (可选): 指定国际证券识别码(ISIN)，这是一个全球唯一的十二位代码，分配给世界范围内每个证券发行
- `listing_date` (可选): 指定上市日期，即新上市实体的第一个交易日
- `ipo_status` (可选): 指定IPO状态
- `order` (可选): 基于排序字段的结果排序，可选值: asc, desc
- `limit` (可选): 限制返回的结果数量，默认为10，最大为1000
- `sort` (可选): 用于排序的字段

#### 响应参数
```json
{
  "next_url": "https://api.polygon.io/v1/reference/ipos?cursor=...", // 如果存在，此值可用于获取下一页数据
  "request_id": "abc123",   // 服务器分配的请求ID
  "results": [              // 包含请求数据的结果数组
    {
      "announced_date": "2021-03-15", // IPO事件宣布的日期
      "currency_code": "USD", // 证券的基础货币
      "final_issue_price": 120.0, // 公司及其承销商在IPO上市前设定的价格
      "highest_offer_price": 125.0, // IPO价格范围内可能用于定价股票的最高价格
      "ipo_status": "history", // IPO事件的状态，可能值包括：direct_listing_process, history, new, pending, postponed, rumor, withdrawn
      "isin": "US1234567890", // 国际证券识别码，全球唯一的十二位代码
      "issuer_name": "Example Company Inc.", // 发行人名称
      "last_updated": "2021-03-25", // IPO事件最后修改的日期
      "listing_date": "2021-03-20", // 新上市实体的第一个交易日
      "lot_size": 100, // 单次交易中可买卖的最小股份数
      "lowest_offer_price": 115.0, // IPO价格范围内公司愿意向投资者提供股票的最低价格
      "max_shares_offered": 10000000, // 公司向投资者提供的上限股份数
      "min_shares_offered": 8000000, // 公司在IPO中愿意出售的下限股份数
      "primary_exchange": "XNYS", // 证券上市的主要交易所的市场标识符代码
      "security_description": "Common Stock", // 证券的描述
      "security_type": "CS", // 股票的分类，例如"CS"代表普通股
      "shares_outstanding": 12000000, // 公司已发行并由投资者持有的股份总数
      "ticker": "EXC", // IPO事件的股票代码
      "total_offer_size": 1200000000, // 公司通过IPO募集的总金额
      "us_code": "123456789" // 北美金融证券的唯一九位字母数字代码
    }
    // 更多IPO...
  ],
  "status": "OK"            // 此请求响应的状态
}
```

#### 用途
此端点适用于：
- IPO研究
- 市场趋势分析
- 投资筛选
- 历史事件比较

参考链接：[Polygon.io IPOs](https://polygon.io/docs/rest/stocks/corporate-actions/ipos)

## 股票拆分 (Splits)

### 请求
```
GET /v3/reference/splits
```

### 描述
获取历史股票拆分事件，包括执行日期和比率因子，以了解一个公司的股份结构随时间的变化。Polygon.io利用这些数据对其他端点(如聚合API)进行价格调整，确保用户可以访问经过调整和未调整的历史价格视图，从而进行更明智的分析。

### 查询参数
- `ticker` (可选): 指定区分大小写的股票代码，例如 AAPL 代表苹果公司
- `execution_date` (可选): 按执行日期查询，格式为 YYYY-MM-DD
- `reverse_split` (可选): 查询反向股票拆分。拆分比率中 split_from 大于 split_to 表示反向拆分。默认情况下不使用此过滤器
- `order` (可选): 基于排序字段的结果排序，可选值: asc, desc
- `limit` (可选): 限制返回的结果数量，默认为10，最大为1000
- `sort` (可选): 用于排序的字段

### 响应参数
```json
{
  "next_url": "https://api.polygon.io/v3/reference/splits?cursor=...", // 如果存在，此值可用于获取下一页数据
  "request_id": "abc123",   // 服务器分配的请求ID
  "results": [              // 包含请求数据的结果数组
    {
      "execution_date": "2022-08-25", // 股票拆分的执行日期。在此日期股票拆分被应用
      "id": "SB123456789", // 此股票拆分的唯一标识符
      "split_from": 1, // 拆分比率中的第二个数字。例如：在2对1拆分中，split_from值为1
      "split_to": 2, // 拆分比率中的第一个数字。例如：在2对1拆分中，split_to值为2
      "ticker": "AAPL" // 股票拆分的股票代码
    }
    // 更多拆分...
  ],
  "status": "OK"            // 此请求响应的状态
}
```

### 用途
此端点适用于：
- 历史分析
- 价格调整
- 数据一致性
- 建模

参考链接：[Polygon.io Splits](https://polygon.io/docs/rest/stocks/corporate-actions/splits)

## 股息 (Dividends)

### 请求
GET /v3/reference/dividends

### 描述
获取给定股票代码的现金股息分配历史记录，包括宣布日期、除息日、登记日和支付日，以及支付金额和频率。该端点整合了关键的股息信息，使用户能够在收益中考虑股息收入，制定以股息为重点的策略，并支持税务报告需求。

### 查询参数
- `ticker` (可选): 指定区分大小写的股票代码，例如 AAPL 代表苹果公司
- `ex_dividend_date` (可选): 按除息日查询，格式为 YYYY-MM-DD
- `record_date` (可选): 按登记日查询，格式为 YYYY-MM-DD
- `declaration_date` (可选): 按宣布日期查询，格式为 YYYY-MM-DD
- `pay_date` (可选): 按支付日期查询，格式为 YYYY-MM-DD
- `frequency` (可选): 按每年支付股息的次数查询。可能值：0(一次性)、1(每年)、2(半年)、4(季度)、12(每月)、24(双月)和52(每周)
- `cash_amount` (可选): 按股息的现金金额查询
- `dividend_type` (可选): 按股息类型查询。已支付和/或预计按一致时间表支付的股息被标记为CD。已支付的特殊现金股息，这些股息不频繁或不寻常，和/或无法预期在未来发生的，被标记为SC
- `order` (可选): 基于排序字段的结果排序，可选值: asc, desc
- `limit` (可选): 限制返回的结果数量，默认为10，最大为1000
- `sort` (可选): 用于排序的字段

### 响应参数
```json
{
  "next_url": "https://api.polygon.io/v3/reference/dividends?cursor=...", // 如果存在，此值可用于获取下一页数据
  "request_id": "abc123",   // 服务器分配的请求ID
  "results": [              // 包含请求数据的结果数组
    {
      "cash_amount": 0.88,  // 每拥有一股的股息现金金额
      "currency": "USD",    // 支付股息的货币
      "declaration_date": "2022-07-28", // 宣布股息的日期
      "dividend_type": "CD", // 股息类型。已支付和/或预计按一致时间表支付的股息被标记为CD。特殊现金股息被标记为SC。长期和短期资本收益分配分别被标记为LT和ST
      "ex_dividend_date": "2022-08-05", // 股票首次不带股息交易的日期，由交易所确定
      "frequency": 4,       // 每年支付股息的次数。可能值：0(一次性)、1(每年)、2(半年)、4(季度)、12(每月)、24(双月)和52(每周)
      "id": "DIV123456789", // 股息的唯一标识符
      "pay_date": "2022-08-18", // 支付股息的日期
      "record_date": "2022-08-08", // 必须持有股票才能获得股息的日期，由公司设定
      "ticker": "AAPL"      // 股息的股票代码
    }
    // 更多股息...
  ],
  "status": "OK"            // 此请求响应的状态
}
```

### 用途
此端点适用于：
- 收入分析
- 总回报计算
- 股息策略
- 税务规划

参考链接：[Polygon.io Dividends](https://polygon.io/docs/rest/stocks/corporate-actions/dividends)