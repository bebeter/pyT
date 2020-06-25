from tqsdk import (
    TqApi,
    TqAccount,
    TqBacktest,
    TargetPosTask,
    TqSim,
    tafunc,
    ta
)
from multiprocessing import Process
from datetime import datetime


class CuatroStrategy(Process):
    ''''''

    author = 'XIAO LI'

    boll_window = 20
    boll_dev = 1.8
    rsi_window = 14
    rsi_signal = 20
    fast_window = 4
    slow_window = 26
    trailing_long = 0.5
    trailing_short = 0.3
    vol = 1

    boll_up = float('nan')
    boll_down = float('nan')
    rsi_value = float('nan')
    rsi_long = float('nan')
    rsi_short = float('nan')
    fast_ma = float('nan')
    slow_ma = float('nan')
    ma_trend = float('nan')
    intra_trade_high = float('nan')
    intra_trade_low = float('nan')
    long_stop = float('nan')
    short_stop = float('nan')

    parameters = [
        'boll_window'
        'boll_dev'
        'rsi_window'
        'rsi_signal'
        'fast_window'
        'slow_window'
        'trailing_long'
        'trailing_short'
        'vol'
    ]

    variables = [
        'boll_up'
        'boll_down'
        'rsi_value'
        'rsi_long'
        'rsi_short'
        'fast_ma'
        'slow_ma'
        'ma_trend'
        'intra_trade_high'
        'intra_trade_low '
        'long_stop'
        'short_stop'
    ]

    def __init__(self, symbol):
        Process.__init__(self)
        self.symbol = symbol
        self.rsi_long = 50 + self.rsi_signal
        self.rsi_short = 50 - self.rsi_signal
        self.api = TqApi(TqSim(init_balance=50000))
        self.now = datetime.now()
        self.target_pos = TargetPosTask(self.api, self.symbol)
        self.ticks = self.api.get_tick_serial(self.symbol)
        self.klines5 = self.api.get_kline_serial(self.symbol, 60 * 5)
        self.klines15 = self.api.get_kline_serial(self.symbol, 60 * 15)
        self.position = self.api.get_position(self.symbol)

    def on_init(self):
        print(self.now, '策略初始化')

    def on_start(self):
        print(self.now, '策略启动')

    def on_stop(self):
        print(self.now, '策略停止')

    def on_tick(self, ticks):
        if self.api.is_changing(ticks, 'datetime'):

            if self.position.pos_long == 0 and self.position.pos_short == 0:

                if self.ma_trend > 0 and self.rsi_value >= self.rsi_long and ticks.iloc[-1].last_price > self.boll_up:
                    self.target_pos.set_target_volume(self.vol)
                    self.intra_trade_high = ticks.iloc[-1].last_price

                if self.ma_trend < 0 and self.rsi_value <= self.rsi_short and ticks.iloc[
                    -1].last_price < self.boll_down:
                    self.target_pos.set_target_volume(-self.vol)
                    self.intra_trade_low = ticks.iloc[-1].last_price

            elif self.position.pos_long > 0:
                self.intra_trade_high = max(self.intra_trade_high, ticks.iloc[-1].last_price)
                self.long_stop = (self.intra_trade_high - self.trailing_long * (self.boll_up - self.boll_down))
                if ticks.iloc[-1].last_price < self.long_stop:
                    self.target_pos.set_target_volume(0)
                    self.intra_trade_high = float('nan')

            else:
                self.intra_trade_low = min(self.intra_trade_low, ticks.iloc[-1].last_price)
                self.short_stop = (self.intra_trade_low + self.trailing_short * (self.boll_up - self.boll_down))
                if ticks.iloc[-1].last_price > self.short_stop:
                    self.target_pos.set_target_volume(0)
                    self.intra_trade_low = float('nan')

    def on_5minbar(self, klines5):
        if self.api.is_changing(klines5, 'datetime'):
            boll = ta.BOLL(klines5.iloc[:-1], self.boll_window, self.boll_dev).iloc[-1]
            self.boll_up = boll['top']
            self.boll_down = boll['bottom']
            self.rsi_value = ta.RSI(klines5.iloc[:-1], self.rsi_window).iloc[-1]['rsi']

    def on_15minbar(self, klines15):
        if self.api.is_changing(klines15, 'datetime'):

            self.fast_ma = ta.SMA(klines15.iloc[:-1], self.fast_window, 2)
            self.slow_ma = ta.SMA(klines15.iloc[:-1], self.slow_window, 2)

            if self.fast_ma > self.slow_ma:
                self.ma_trend = 1
            elif self.fast_ma < self.slow_ma:
                self.ma_trend = -1
            else:
                self.ma_trend = 0

    def on_order(self):
        if self.api.is_changing(self.api.get_order()):
            pass

    def on_trade(self):
        if self.api.is_changing(self.api.get_trade()):
            pass

    def run(self):
        self.on_init()
        self.on_start()
        while True:
            self.api.wait_update()
            self.on_tick(self.ticks)
            self.on_5minbar(self.klines5)
            self.on_15minbar(self.klines15)
            self.on_order()
            self.on_trade()
        self.on_stop()


if __name__ == '__main__':
    p1 = CuatroStrategy('CZCE.SR009')
    p1.run()
    p1.join()