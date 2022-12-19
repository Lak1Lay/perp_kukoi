import schedule
import time
from kukoin import Client
from telegram.ext import Updater, CommandHandler

# Replace TOKEN with your bot's token and YOUR_CHAT_ID with the chat ID you want to send the messages to
updater = Updater(token='TOKEN', use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id='YOUR_CHAT_ID', text='I am a bot that will send you updates on the BTC/USDT index perpetual MACD indicator on Kucoin.')

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def check_crossing():
  # Replace YOUR_API_KEY and YOUR_API_SECRET with your Kucoin API key and secret
  client = Client(api_key='YOUR_API_KEY', api_secret='YOUR_API_SECRET')

  # Retrieve the klines for the current and previous 15 minute candles
  klines = client.futures.klines(symbol='BTC-USDT', interval='15min')
  prev_klines = client.futures.klines(symbol='BTC-USDT', interval='15min', limit=2)

  # Extract the close price of the current and previous candles
  current_close = float(klines[0][4])
  prev_close = float(prev_klines[1][4])

  # Calculate the change in price since the previous candle
  price_change = current_close - prev_close

  # Retrieve the MACD and signal line data for the current candle
  macd = klines[0][6]
  signal = klines[0][7]

  # Extract the MACD and signal line data for the previous candle
  prev_macd = prev_klines[1][6]
  prev_signal = prev_klines[1][7]

  # Check if the MACD line has crossed the signal line
  if macd > signal and prev_macd < prev_signal:
    # Check if the price has gone up since the previous candle
    if price_change > 0:
      text = 'The MACD line just crossed above the signal line in an ascending direction (towards the top) and the price has gone up on BTC/USDT index perpetual on Kucoin on the 15 minute timeframe!'
    else:
      text = 'The MACD line just crossed above the signal line in an ascending direction (towards the top) and the price has gone down on BTC/USDT index perpetual on Kucoin on the 15 minute timeframe!'
    context.bot.send_message(chat_id='YOUR_CHAT_ID', text=text)
  elif macd < signal and prev_macd > prev_signal:
    # Check if the price has gone down since the previous candle
    if price_change < 0:
      text = 'The MACD line just crossed below the signal line in a descending direction (towards the bottom) and the price has gone down on BTC/USDT index perpetual on Kucoin on the 15 minute timeframe!'
    else:
      text = 'The MACD line just crossed below the signal line in a descending direction (towards the bottom) and the price has gone up on BTC/USDT index perpetual on Kucoin on the 15 minute timeframe!'
context.bot.send_message(chat_id='YOUR_CHAT_ID', text=text)
else:
  # The MACD line has not crossed the signal line, so check if the MACD line is increasing or decreasing
  if macd > prev_macd:
    # Check if the price has gone up since the previous candle
    if price_change > 0:
      text = 'The MACD line is increasing and the price has gone up on BTC/USDT index perpetual on Kucoin on the 15 minute timeframe!'
    else:
      text = 'The MACD line is increasing and the price has gone down on BTC/USDT index perpetual on Kucoin on the 15 minute timeframe!'
  elif macd < prev_macd:
    # Check if the price has gone down since the previous candle
    if price_change < 0:
      text = 'The MACD line is decreasing and the price has gone down on BTC/USDT index perpetual on Kucoin on the 15 minute timeframe!'
    else:
      text = 'The MACD line is decreasing and the price has gone up on BTC/USDT index perpetual on Kucoin on the 15 minute timeframe!'
  else:
    # The MACD line has not changed, so check if the price has gone up or down since the previous candle
    if price_change > 0:
      text = 'The MACD line has not changed and the price has gone up on BTC/USDT index perpetual on Kucoin on the 15 minute timeframe!'
    elif price_change < 0:
      text = 'The MACD line has not changed and the price has gone down on BTC/USDT index perpetual on Kucoin on the 15 minute timeframe!'
    else:
      text = 'The MACD line has not changed and the price has not changed on BTC/USDT index perpetual on Kucoin on the 15 minute timeframe!'
    context.bot.send_message(chat_id='YOUR_CHAT_ID', text=text)

# Run the check_crossing function every 15 minutes
schedule.every(1).minutes.do(check_crossing)

while True:
  schedule.run_pending()
  time.sleep(1)

