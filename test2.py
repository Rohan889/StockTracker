import btalib 
import pandas as pd


df = pd.read_csv('data.txt',parse_dates =  True, index_col = 'Date')       
rsi = btalib.rsi(df)
rsi = rsi.df
rsi1 = rsi.to_numpy()
print(rsi)