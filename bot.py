import alpaca_trade_api as tradeapi
import websocket
import requests, json
import btalib
import pandas as pd
from datetime import datetime


from test import *
file13 = open("data.txt", "w")
file13.close()
minute = 0 
print(1)
def connection():
    api = tradeapi.REST(API_KEY, SECRET_KEY, aplaca_endpoint)
    r = requests.get(aplaca_endpoint)
    account = api.get_account()
    #print(r.content) 
    print(r.headers)  
    print(account.status)
    
def on_open(ws):
    global minute
    minute = 0
    print("opened")
    auth_data = {"action": "auth", 
                 "key": API_KEY, 
                 "secret": SECRET_KEY
                 }
    ws.send(json.dumps(auth_data))
    message = {"action": "subscribe", "trades": [], "quotes": [], "bars": ["AAPL"]}
    ws.send(json .dumps(message))


def on_message(ws,message):
    global minute 
   
    print(minute)
    print( "This is the message" + message) 
    
    if(message[11] == 'S'): 
        write_message(message, symbol)
        
        m = minute 
        minute = m + 1
        if(minute > 21):
            print("Minute is over 21")
            check_buy()

   

    
    #write_message(message)
    #read_message()
def check_buy():
    global minute 
    m = minute
    get_sma()
    get_rsi()
     
def check_sell():
    print("Sell")
def get_rsi():
    global minute 
    m = minute
    print("checking rsi ")
    try:
        df = pd.read_csv('data.txt',parse_dates =  True, index_col = 'Date')
        
        rsi = btalib.rsi(df)
        rsi = rsi.df
        rsi1 = rsi.to_numpy()
        print("This is rsi")
        print(rsi)
        #print(rsi1[m])
    except:
        pass
    
    
def get_sma():
    global minute
    m = minute
    df = pd.read_csv('data.txt',parse_dates =  True, index_col = 'Date')
    sma = btalib.sma(df,period = 2)
    print(sma.df)
    sma1 = sma.df
    sma1 = sma1.to_numpy()
    #print(sma1[m][0])
    #print("This is sma" + sma)
    
def order(sb, qt, s, typ, t):
    api = tradeapi.REST(API_KEY, SECRET_KEY, aplaca_endpoint)
    account = api.get_account()
    order = api.submit_order(symbol= sb,
                        qty = qt,  
                        side = s,
                        type = typ,
                        time_in_force = t)
    print(order)
def read_message():
    print("This is file reading" + file13.readline())

def write_message(message, ticker):
    file12 = open("data.txt","a")
    
    if(message[0] == "D"):
        file12.write(message)
    else:
        
        time = datetime.now()
        time = str(time)
        #print(time.strip() + "hi")
        if(message[15:19] == ticker):
            index1 = message.find('"o":')
            
            index2 = message.find('"c":')
            index3 = message.find('"h":')
            index4 = message.find('"l":')
            index5 = message.find('"v":')
            index6 = message.find('"t":')
            open_price = message[index1+4:index2-1]
            close_price = message[index2+4:index3-1]
            high_price = message[index3+4:index4-1]
            low_price = message[index4+4:index5-1]
            volume = message[index5+4:index6-1]
            print(open_price)
            file12.write(time + "," + open_price + "," + close_price + "," +high_price + "," + low_price + "," + volume + "," + "0\n" )


connection()
write_message("Date,Open,High,Low,Close,Volume,OpenInterest\n", symbol)
socket = "wss://stream.data.alpaca.markets/v2/iex"
ws = websocket.WebSocketApp(socket,on_open=on_open, on_message=on_message)
ws.run_forever()

#aapl = api.get_barset('AAPL', 'day')
#print(aapl.df)
# Just some notes. Make this so that they have to plug in their alpeca id and secret key and then it runs. 