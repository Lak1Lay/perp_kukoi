import requests
import json
import time
from websocket import create_connection

# Replace YOUR_BOT_TOKEN with the API key for your Telegram bot
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Replace YOUR_CHAT_ID with the chat ID of the recipient for the messages
CHAT_ID = "YOUR_CHAT_ID"

def send_message(text):
    """Sends a message to the specified chat ID using the Telegram API"""
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data=data)

def calculate_macd(data):
    """Calculates the MACD line and signal line based on the given data"""
    # Calculate the 12-day EMA
    ema_12 = sum(data[-12:]) / 12
    # Calculate the 26-day EMA
    ema_26 = sum(data[-26:]) / 26
    # Calculate the MACD line
    macd_line = ema_12 - ema_26
    # Calculate the 9-day EMA of the MACD line
    signal_line = sum(macd_line[-9:]) / 9
    return macd_line, signal_line

def check_crossing(prev_macd, macd, prev_signal, signal):
    """Checks if the MACD line has crossed the signal line in an upward or downward direction"""
    if prev_macd < prev_signal and macd > signal:
        return "upward"
    elif prev_macd > prev_signal and macd < signal:
        return "downward"
    return None

def check_price_change(prev_price, price):
    """Checks if the price has gone up or down since the last message was sent"""
    if price > prev_price:
        return "up"
    elif price < prev_price:
        return "down"
    return None

ws = create_connection("wss://fstream.kucoin.com/ws/v1")

# Subscribe to the BTC USDT perpetual data feed
subscribe_data = {
    "id": "subscribe",
    "type": "subscribe",
    "topic": "market.BTC-USDT.kline.15min"
}
ws.send(json.dumps(subscribe_data))

# Initialize variables to store previous MACD and signal line values and previous price
prev_macd = None
prev_signal = None
prev_price = None

while True:
    data = json.loads(ws.recv())
    # Check if the data is a kline (candlestick)
    if "data" in data and "kline" in data["data"]:
        kline = data["data"]["kline"]
        # Get the close price from the kline
        price = kline["close"]
        # Check if the price has changed since the last message was sent
       price_change = check_price_change(prev_price, price)
if price_change is not None:
    send_message(f"Price has gone {price_change} since the last message")
    prev_price = price

# Calculate the MACD line and signal line
macd_line, signal_line = calculate_macd(data)

# Check if the MACD line has crossed the signal line
crossing = check_crossing(prev_macd, macd_line, prev_signal, signal_line)
if crossing is not None:
    send_message(f"MACD line has crossed the signal line in a {crossing} direction")
    prev_macd = macd_line
    prev_signal = signal_line

# Sleep for one minute before checking again
time.sleep(60)
