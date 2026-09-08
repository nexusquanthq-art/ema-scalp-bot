# core/risk.py

from config.settings import RISK_PERCENT, LEVERAGE

class RiskManager:
    def __init__(self, exchange, account_name):
        self.exchange = exchange
        self.account_name = account_name
    
    def get_balance(self):
        balance = self.exchange.fetch_balance()
        return balance['total'].get('USDT', 0)
    
    def calculate_position_size(self, entry, stop_loss, signal_type):
        balance = self.get_balance()
        risk_amount = balance * (RISK_PERCENT / 100)
        
        sl_distance_percent = abs(entry - stop_loss) / entry
        
        if sl_distance_percent == 0:
            return 0
        
        position_value = (risk_amount * LEVERAGE) / sl_distance_percent
        position_size = position_value / entry
        
        return round(position_size, 4)