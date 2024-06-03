import ccxt
import time
import pybroker

class CryptoArbitrageBot:
    def __init__(self, exchanges):
        self.exchanges = exchanges

    def fetch_order_book(self, symbol, exchange):
        order_book = exchange.fetch_order_book(symbol)
        return order_book['bids'], order_book['asks']

    def find_arbitrage_opportunity(self, symbol):
        opportunities = []
        for exchange_name, exchange in self.exchanges.items():
            for compare_exchange_name, compare_exchange in self.exchanges.items():
                if exchange_name != compare_exchange_name:
                    bids, asks = self.fetch_order_book(symbol, exchange)
                    compare_bids, compare_asks = self.fetch_order_book(symbol, compare_exchange)
                    best_bid = bids[0][0] if bids else None
                    best_ask = asks[0][0] if asks else None
                    compare_best_bid = compare_bids[0][0] if compare_bids else None
                    compare_best_ask = compare_asks[0][0] if compare_asks else None
                    if best_bid and compare_best_ask and best_bid > compare_best_ask:
                        opportunities.append({
                            'buy_exchange': exchange_name,
                            'sell_exchange': compare_exchange_name,
                            'profit': best_bid - compare_best_ask
                        })
        return opportunities

    def execute_arbitrage(self, symbol, opportunity):
        buy_exchange = self.exchanges[opportunity['buy_exchange']]
        sell_exchange = self.exchanges[opportunity['sell_exchange']]
        amount_to_buy = 1  # Example: Buy 1 unit of cryptocurrency
        buy_price = buy_exchange.fetch_order_book(symbol)['asks'][0][0]
        sell_price = sell_exchange.fetch_order_book(symbol)['bids'][0][0]
        # Example: Execute buy order on buy_exchange and sell order on sell_exchange
        buy_exchange.create_order(symbol, 'limit', 'buy', amount_to_buy, buy_price)
        sell_exchange.create_order(symbol, 'limit', 'sell', amount_to_buy, sell_price)
        print(f"Arbitrage opportunity executed: Buy at {buy_price} on {opportunity['buy_exchange']} and sell at {sell_price} on {opportunity['sell_exchange']}")

def main():
    # Initialize exchanges (replace with your API keys)
    exchange1 = ccxt.binance({'apiKey': 'YOUR_API_KEY', 'secret': 'YOUR_SECRET'})
    exchange2 = ccxt.bittrex({'apiKey': 'YOUR_API_KEY', 'secret': 'YOUR_SECRET'})
    
    exchanges = {'Binance': exchange1, 'Bittrex': exchange2}
    bot = CryptoArbitrageBot(exchanges)
    
    symbol = 'BTC/USDT'  # Example trading pair
    while True:
        opportunities = bot.find_arbitrage_opportunity(symbol)
        if opportunities:
            best_opportunity = max(opportunities, key=lambda x: x['profit'])
            bot.execute_arbitrage(symbol, best_opportunity)
        time.sleep(60)  # Check for arbitrage opportunities every minute

if __name__ == "__main__":
    main()
