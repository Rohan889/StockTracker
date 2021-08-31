import alpaca_trade_api as tradeapi
from test import *
api = tradeapi.REST(API_KEY, SECRET_KEY, aplaca_endpoint)

# Get our account information.
account = api.get_account()
print()
# Check if our account is restricted from trading.
if account.trading_blocked:
    print('Account is currently restricted from trading.')

# Check how much money we can use to open new positions.
print('${} is available as buying power.'.format(account.buying_power))

# Check if AAPL is tradable on the Alpaca platform.
aapl_asset = api.get_asset('AAPL')
if aapl_asset.tradable:
    print('We can trade AAPL.')



