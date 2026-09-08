# core/kill_switch.py


from datetime import datetime, timedelta

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class KillSwitch:
    def __init__(self):
        self.max_consecutive_losses = 3       
        self.max_trades_per_hour = 5          
        self.cooldown_minutes = 60          
        self.consecutive_losses = 0
        self.trade_timestamps = []
        self.banned_until = None
        self.total_trades = 0
        self.total_wins = 0
        self.total_losses = 0
    
    def record_win(self):
        self.consecutive_losses = 0
        self.total_wins += 1
        self.total_trades += 1
        self.trade_timestamps.append(datetime.now())
        logging.info(f"✅ Kill Switch: Win! Consecutive losses reset to 0")
    
    def record_loss(self):
        self.consecutive_losses += 1
        self.total_losses += 1
        self.total_trades += 1
        self.trade_timestamps.append(datetime.now())
        
        logging.info(f"❌ Kill Switch: Loss! Consecutive losses: {self.consecutive_losses}")
        
        if self.consecutive_losses >= self.max_consecutive_losses:
            self.banned_until = datetime.now() + timedelta(minutes=self.cooldown_minutes)
            logging.warning(f"🛑 KILL SWITCH ACTIVATED! {self.consecutive_losses} losses. Banned until {self.banned_until.strftime('%H:%M:%S')}")
    
    def is_banned(self):
        
        now = datetime.now()

        if self.banned_until and now < self.banned_until:
            return True
        
    
        if self.banned_until and now >= self.banned_until:
            self.banned_until = None
            self.consecutive_losses = 0
            logging.info("🔓 Kill Switch: Ban expired. Bot is free!")
        
        one_hour_ago = now - timedelta(hours=1)
        recent_trades = [t for t in self.trade_timestamps if t > one_hour_ago]
        self.trade_timestamps = recent_trades    
        
        if len(recent_trades) >= self.max_trades_per_hour:
            self.banned_until = now + timedelta(minutes=self.cooldown_minutes)
            logging.warning(f"🛑 KILL SWITCH: {len(recent_trades)} trades in 1 hour! Banned until {self.banned_until.strftime('%H:%M:%S')}")
            return True
        
        return False
    
    def get_status(self):
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)
        recent = len([t for t in self.trade_timestamps if t > one_hour_ago])
        
        return {
            'consecutive_losses': self.consecutive_losses,
            'trades_last_hour': recent,
            'total_trades': self.total_trades,
            'wins': self.total_wins,
            'losses': self.total_losses,
            'banned': self.is_banned(),
            'banned_until': self.banned_until
        }