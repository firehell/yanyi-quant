package main

import (
	"encoding/json"
	"log"
	"net/url"
	"os"
	"os/signal"
	"sync"
	"time"

	"github.com/gorilla/websocket"
)

const (
	websocketURL = "wss://socket.polygon.io/stocks"
)

// Aggregation represents the structure for aggregated data
type Aggregation struct {
	EV  string  `json:"ev"`  // Event Type
	Sym string  `json:"sym"` // Symbol
	V   int64   `json:"v"`   // Volume
	AV  int64   `json:"av"`  // Accumulated Volume
	Op  float64 `json:"op"`  // Official Open Price
	VW  float64 `json:"vw"`  // Volume Weighted Average Price
	O   float64 `json:"o"`   // Open Price
	C   float64 `json:"c"`   // Close Price
	H   float64 `json:"h"`   // High Price
	L   float64 `json:"l"`   // Low Price
	A   float64 `json:"a"`   // Accumulated VWAP
	S   int64   `json:"s"`   // Start Timestamp (Unix ms)
	E   int64   `json:"e"`   // End Timestamp (Unix ms)
	Z   int64   `json:"z"`   // Average Trade Size
	OTC bool    `json:"otc"` // Over-the-counter trade
}

// WebSocketMessage represents the structure for incoming WebSocket messages
type WebSocketMessage struct {
	Action  string      `json:"action"`
	Params  string      `json:"params"`
	Data    Aggregation `json:"data"` // For some message types
	Ev      string      `json:"ev"`   // For status messages
	Status  string      `json:"status"`
	Message string      `json:"message"`
}

// FiveMinuteData stores aggregated data for a 5-minute interval
type FiveMinuteData struct {
	Open      float64
	High      float64
	Low       float64
	Close     float64
	Volume    int64
	StartTime time.Time
	EndTime   time.Time
}

func main() {
	apiKey := os.Getenv("_tpwPsCcsASx5DcrD1NpUEA1NHxqr5gt") // Replace with your actual API key or environment variable
	if apiKey == "" {
		log.Fatal("POLYGON_API_KEY environment variable not set")
		return
	}

	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt)

	u := url.URL{Scheme: "wss", Host: "socket.polygon.io", Path: "/stocks"}
	log.Printf("connecting to %s", u.String())

	c, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		log.Fatalf("dial: %v", err)
	}
	defer c.Close()

	done := make(chan struct{})

	go func() {
		defer close(done)
		for {
			_, message, err := c.ReadMessage()
			if err != nil {
				log.Println("read:", err)
				return
			}
			log.Printf("recv: %s", message)

			var msg WebSocketMessage
			if err := json.Unmarshal(message, &msg); err == nil {
				if msg.Ev == "status" {
					log.Printf("Status: %s - %s", msg.Status, msg.Message)
				} else if len(msg.Data) > 0 && msg.Data[0].EV == "AM" {
					for _, agg := range msg.Data {
						processMinuteAggregation(agg)
					}
				}
			} else {
				log.Println("error unmarshalling message:", err)
			}
		}
	}()

	// Authenticate
	authMessage := WebSocketMessage{Action: "auth", Params: apiKey}
	authJSON, _ := json.Marshal(authMessage)
	err = c.WriteMessage(websocket.TextMessage, authJSON)
	if err != nil {
		log.Println("write auth:", err)
		return
	}

	// Subscribe to all stocks' minute aggregates
	subscribeMessage := WebSocketMessage{Action: "subscribe", Params: "AM.*"}
	subscribeJSON, _ := json.Marshal(subscribeMessage)
	err = c.WriteMessage(websocket.TextMessage, subscribeJSON)
	if err != nil {
		log.Println("write subscribe:", err)
		return
	}

	for {
		select {
		case <-done:
			return
		case <-interrupt:
			log.Println("interrupt")

			// Cleanly close the connection by sending a close message and then
			// waiting for the server to close the connection.
			err := c.WriteMessage(websocket.CloseMessage, websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""))
			if err != nil {
				log.Println("write close:", err)
				return
			}
			select {
			case <-done:
			case <-time.After(time.Second):
			}
			return
		}
	}
}

var (
	fiveMinuteAggregations = make(map[string]Aggregation)
	aggregationMutex       sync.Mutex
)

func processMinuteAggregation(agg Aggregation) {
	aggregationMutex.Lock()
	defer aggregationMutex.Unlock()

	if _, ok := fiveMinuteAggregations[agg.Sym]; !ok {
		fiveMinuteAggregations[agg.Sym] = Aggregation{}
	}
	fiveMinuteAggregations[agg.Sym] = append(fiveMinuteAggregations[agg.Sym], agg)

	// Check if we have enough data for a 5-minute aggregation
	if len(fiveMinuteAggregations[agg.Sym]) >= 5 {
		aggregateFiveMinuteData(agg.Sym)
		delete(fiveMinuteAggregations, agg.Sym) // Clear the buffer for this symbol
	}
}

func aggregateFiveMinuteData(symbol string) {
	aggregationMutex.Lock()
	defer aggregationMutex.Unlock()

	if len(fiveMinuteAggregations[symbol]) == 0 {
		return
	}

	var (
		openPrice   float64
		highPrice   float64
		lowPrice    float64
		closePrice  float64
		totalVolume int64
		startTime   time.Time
		endTime     time.Time
		first       = true
	)

	for _, agg := range fiveMinuteAggregations[symbol] {
		currentTime := time.Unix(agg.S/1000, (agg.S%1000)*1000000)

		if first {
			openPrice = agg.O
			highPrice = agg.H
			lowPrice = agg.L
			startTime = currentTime
			first = false
		} else {
			if agg.H > highPrice {
				highPrice = agg.H
			}
			if agg.L < lowPrice {
				lowPrice = agg.L
			}
		}
		closePrice = agg.C
		totalVolume += agg.V
		endTime = time.Unix(agg.E/1000, (agg.E%1000)*1000000)
	}

	log.Printf("5-Minute Aggregation for %s: Open=%.2f, High=%.2f, Low=%.2f, Close=%.2f, Volume=%d, StartTime=%s, EndTime=%s",
		symbol, openPrice, highPrice, lowPrice, closePrice, totalVolume, startTime.Format(time.RFC3339), endTime.Format(time.RFC3339))

	// TODO: Here you would typically store this 5-minute aggregated data (e.g., in a database)
}
