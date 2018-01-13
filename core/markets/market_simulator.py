from core.markets.market import Market
from core.database import ohlcv_functions

class MarketSimulator(Market):
    """Wrapper for market that allows simulating simple buys and sells and market price"""
    def __init__(self, exchange, base_currency, quote_currency, quote_currency_balance):
        super().__init__(exchange, base_currency, quote_currency)
        self.starting_balance = quote_currency_balance
        self.quote_balance = quote_currency_balance
        self.base_balance = 0

    def buy(self, quantity):
        if self.quote_balance >= quantity * self.get_ask_price():
            self.quote_balance = self.quote_balance - quantity * self.get_ask_price()
            self.base_balance = self.base_balance + quantity
            print()
            print("Executed buy simulation of " + str(quantity) + " " + self.base_currency + " for " + str(self.get_ask_price()) + " " + self.quote_currency)
            print(self.quote_currency + " balance: " + str(self.quote_balance))
            print(self.base_currency + " balance: " + str(self.base_balance))
            print()
        else:
            print("Insufficient balance for simulation buy")

    def sell(self, quantity):
        if self.base_balance >= quantity:
            self.base_balance = self.base_balance - quantity
            self.quote_balance = self.quote_balance + quantity * self.get_bid_price()
            print()
            print("Executed sell simulation of " + str(quantity) + " " + self.base_currency + " for " + str(self.get_bid_price()) + " " + self.quote_currency)
            print(self.quote_currency + " balance: " + str(self.quote_balance))
            print(self.base_currency + " balance: " + str(self.base_balance))
            print()
        else:
            print("Insufficient balance for simulation sell")

    def get_ask_price(self):
        """Get ask price for simulation"""
        if self.historical_loaded:
            """if operating on live data, use actual ask"""
            return self.exchange.fetchTicker(self.analysis_pair)['ask']
        else:
            """if operating on historical data, use close"""
            return self.latest_candle['5m'][4]

    def get_bid_price(self):
        if self.historical_loaded:
            """if operating on live data, use actual ask"""
            return self.exchange.fetchTicker(self.analysis_pair)['bid']
        else:
            """if operating on historical data, use close"""
            return self.latest_candle['5m'][4]

    def load_historical(self, interval):
        self._jobs.put(lambda: self._load_historical(interval))

    def _load_historical(self, interval):
        """Load all historical candles to database"""
        print('Getting historical candles for market...')
        data = self.exchange.fetch_ohlcv(self.analysis_pair, interval)
        for entry in data:
            ohlcv_functions.insert_data_into_ohlcv_table(self.exchange.id, self.analysis_pair, interval, entry)
            self.latest_candle[interval] = entry
            self._do_ta_calculations(interval)
            self._tick_strategies()
            print('Writing candle ' + str(entry[0]) + ' to database')
        self.historical_loaded = True
        print('Historical data has been loaded.')
