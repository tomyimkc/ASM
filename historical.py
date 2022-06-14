import statistics
import yfinance as yf 
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# name=input('Ticker name:')
# ticker = yf.Ticker(name)

ticker= yf.Ticker('tsla')
data = ticker.history(interval='5m')

# data = ticker.history()
# data = yf.download(['GOOG','META'], period='1mo')
# data.head()

print(data.columns)
print(data['Volume'])


df_difference=data['High']-data['Low']
print(data.head())
print(df_difference)
HL_list=df_difference.tolist()
volume_list=data['Volume'].tolist()

slope, intercept, r, p, std_err = stats.linregress(HL_list, volume_list)

def myfunc(HL_list):
  return slope * HL_list + intercept

mymodel = list(map(myfunc, HL_list))

print (slope,intercept)

volume_mean=statistics.mean(volume_list)
print (volume_mean)

HL_predict=(volume_mean-intercept)/slope

def HL(volume):
  return (volume-intercept)/slope

print (HL(500000))

plt.scatter(HL_list, volume_list)
plt.plot(HL_list, mymodel)
plt.show()

# print(volume_list)