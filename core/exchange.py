# core/exchange.py

import ccxt
from config.accounts import ACCOUNTS

class ExchangeManager:
    def __init__(self):
        self.exchanges = {}
        self._init_exchanges()
    
    def _init_exchanges(self):
        for acc in ACCOUNTS:
            exchange_class = getattr(ccxt, acc['exchange'])
            
            exchange = exchange_class({
                'apiKey': acc['api_key'],
                'secret': acc['api_secret'],
                'enableRateLimit': True,
            })
            
            if acc.get('testnet'):
                exchange.set_sandbox_mode(True)
            
            self.exchanges[acc['name']] = {
                'exchange': exchange,
                'config': acc
            }
            
            print(f"✓ Connected to {acc['exchange']} - {acc['name']}")
    
    def get_exchange(self, account_name):
        return self.exchanges[account_name]['exchange']
    
    def get_all_accounts(self):
        return list(self.exchanges.keys())