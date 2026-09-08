# core/executor.py


from config.settings import MAX_OPEN_TRADES, SYMBOLS, LEVERAGE

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TradeExecutor:
    def __init__(self, exchange_manager):
        self.em = exchange_manager
    
    def set_leverage(self, exchange, symbol):
        try:
            exchange.set_leverage(LEVERAGE, symbol)
        except:
            pass
    
    def count_open_trades(self, account_name):
        exchange = self.em.get_exchange(account_name)
        positions = exchange.fetch_positions(symbols=SYMBOLS)
        return len([p for p in positions if float(p['contracts']) > 0])
    
    def execute_trade(self, account_name, signal):
        try:
            exchange = self.em.get_exchange(account_name)
            
            if self.count_open_trades(account_name) >= MAX_OPEN_TRADES:
                logging.info(f"Max trades reached for {account_name}")
                return False
            
            symbol = signal.get('symbol', 'BTC/USDT')
            
            self.set_leverage(exchange, symbol)
            
            from core.risk import RiskManager
            rm = RiskManager(exchange, account_name)
            size = rm.calculate_position_size(signal['entry'], signal['stop_loss'], signal['type'])
            
            if size <= 0:
                return False
            
            if signal['type'] == 'BULLISH':
                side = 'buy'
            else:
                side = 'sell'
            
            order = exchange.create_order(
                symbol=symbol,
                type='market',
                side=side,
                amount=size,
                params={
                    'stopLoss': {'triggerPrice': signal['stop_loss']},
                    'takeProfit': {'triggerPrice': signal['take_profit']}
                }
            )
            
            logging.info(f"""
            ⚡ SCALP TRADE
            {signal['type']} {symbol}
            Entry: {signal['entry']:.4f}
            SL: {signal['stop_loss']:.4f}
            TP: {signal['take_profit']:.4f}
            Size: {size} | Leverage: {LEVERAGE}x
            """)
            
            return True
            
        except Exception as e:
            logging.error(f"Trade failed: {e}")
            return False