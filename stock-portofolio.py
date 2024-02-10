import requests

class StockPortfolio:
    def __init__(self):
        self.portfolio = {}

    def add_stock(self, symbol, shares):
        if symbol in self.portfolio:
            self.portfolio[symbol]['shares'] += shares
        else:
            self.portfolio[symbol] = {'shares': shares, 'price': self.get_stock_price(symbol)}

    def remove_stock(self, symbol, shares):
        if symbol in self.portfolio:
            if shares >= self.portfolio[symbol]['shares']:
                del self.portfolio[symbol]
            else:
                self.portfolio[symbol]['shares'] -= shares

    def get_stock_price(self, symbol):
        # Use Alpha Vantage API to get real-time stock price
        api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()
        if 'Global Quote' in data:
            return float(data['Global Quote']['05. price'])
        else:
            return None

    def get_portfolio_value(self):
        total_value = 0
        for symbol, stock_info in self.portfolio.items():
            price = stock_info['price']
            shares = stock_info['shares']
            total_value += price * shares
        return total_value

    def track_performance(self):
        print("Stock Portfolio Performance:")
        for symbol, stock_info in self.portfolio.items():
            price = stock_info['price']
            shares = stock_info['shares']
            current_value = price * shares
            print(f"{symbol}: Shares - {shares}, Current Price - ${price}, Current Value - ${current_value:.2f}")

# Example usage
portfolio = StockPortfolio()
portfolio.add_stock('AAPL', 10)
portfolio.add_stock('GOOGL', 5)
portfolio.track_performance()

portfolio.add_stock('AAPL', 5)
portfolio.remove_stock('GOOGL', 2)
portfolio.track_performance()

print("Total Portfolio Value:", portfolio.get_portfolio_value())
