# core/auto_withdraw.py

import logging
from datetime import datetime
from config.settings import (
    AUTO_WITHDRAW_ENABLED, AUTO_WITHDRAW_PERCENT,
    AUTO_WITHDRAW_MIN_PROFIT, AUTO_WITHDRAW_COIN,
    AUTO_WITHDRAW_NETWORK, AUTO_WITHDRAW_ADDRESS
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)

class AutoWithdraw:
    def __init__(self, exchange_manager):
        self.em = exchange_manager
        self.total_withdrawn = 0
    
    def get_realized_pnl(self, account_name):
        try:
            exchange = self.em.get_exchange(account_name)
            trades = exchange.fetch_my_trades(limit=50)
            pnl = 0
            for t in trades:
                if t.get('info', {}).get('realizedPnl'):
                    pnl += float(t['info']['realizedPnl'])
            return pnl
        except:
            return 0
    
    def get_balance(self, account_name, coin="USDT"):
        try:
            exchange = self.em.get_exchange(account_name)
            return exchange.fetch_balance()['total'].get(coin, 0)
        except:
            return 0
    
    def process_withdraw(self, account_name, profit_amount):
        if not AUTO_WITHDRAW_ENABLED or not AUTO_WITHDRAW_ADDRESS:
            return False
        if profit_amount < AUTO_WITHDRAW_MIN_PROFIT:
            return False
        
        withdraw_amount = profit_amount * (AUTO_WITHDRAW_PERCENT / 100)
        balance = self.get_balance(account_name, AUTO_WITHDRAW_COIN)
        
        if balance < withdraw_amount:
            return False
        
        try:
            exchange = self.em.get_exchange(account_name)
            exchange.withdraw(
                code=AUTO_WITHDRAW_COIN,
                amount=withdraw_amount,
                address=AUTO_WITHDRAW_ADDRESS,
                params={'network': AUTO_WITHDRAW_NETWORK}
            )
            self.total_withdrawn += withdraw_amount
            logging.info(f"💰 Withdrew ${withdraw_amount:.2f} to wallet")
            return True
        except Exception as e:
            logging.error(f"Withdraw failed: {e}")
            return False