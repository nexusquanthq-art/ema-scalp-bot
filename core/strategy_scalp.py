# core/strategy_scalp.py
"""
EMA Pullback Scalp Strategy
Author: Nexus
License: All Rights Reserved

Strategy Logic:
- Uptrend: EMA 20 > EMA 50
- Price pulls back to EMA 20
- Bullish candle with volume confirmation
- Stop loss below recent low minus ATR buffer
- Take profit at 1:2 risk/reward
"""
import pandas as pd
import numpy as np

class ScalpStrategy:
    
    def __init__(self, df):
        self.df = df.copy()
        self._calculate_indicators()
    
    def _calculate_indicators(self):
        df = self.df
        
        # EMA
        df['ema_20'] = df['close'].ewm(span=20, adjust=False).mean()
        df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()

        high_low = df['high'] - df['low']
        high_close = abs(df['high'] - df['close'].shift(1))
        low_close = abs(df['low'] - df['close'].shift(1))
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['atr'] = true_range.ewm(span=14, adjust=False).mean()
        
        df['vol_sma'] = df['volume'].rolling(20).mean()
        df['vol_ratio'] = df['volume'] / df['vol_sma']
    
    def analyze(self):
        """Pullback to EMA 20"""
        df = self.df
        if len(df) < 60:
            return None
        
        last = df.iloc[-1]
        prev = df.iloc[-2]
        prev2 = df.iloc[-3]
        
        if last['ema_20'] > last['ema_50']:
            if prev2['low'] > prev2['ema_20']:
                if abs(prev['low'] - prev['ema_20']) / prev['ema_20'] < 0.003:
                    if last['close'] > last['open'] and last['vol_ratio'] > 0.8:
                        sl = min(prev['low'], last['low']) - last['atr'] * 0.3
                        tp = last['close'] + (last['close'] - sl) * 2  # 1:2
                        return {'type': 'BULLISH', 'entry': last['close'], 'stop_loss': sl, 'take_profit': tp}

        if last['ema_20'] < last['ema_50']:
            if prev2['high'] < prev2['ema_20']:
                if abs(prev['high'] - prev['ema_20']) / prev['ema_20'] < 0.003:
                    if last['close'] < last['open'] and last['vol_ratio'] > 0.8:
                        sl = max(prev['high'], last['high']) + last['atr'] * 0.3
                        tp = last['close'] - (sl - last['close']) * 2  # 1:2
                        return {'type': 'BEARISH', 'entry': last['close'], 'stop_loss': sl, 'take_profit': tp}
        
        return None