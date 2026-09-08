# core/data.py

import pandas as pd
from config.settings import TIMEFRAME

class DataFetcher:
    def __init__(self, exchange):
        self.exchange = exchange
    
    def get_data(self, symbol, limit=100):
        candles = self.exchange.fetch_ohlcv(symbol, timeframe=TIMEFRAME, limit=limit)
        
        df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        return df