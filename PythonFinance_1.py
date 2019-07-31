#Use python to find the stock price of Tesla from 2010-06-29 to 2019-07-28.
#Step 1: set up external libraries
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
#Step 2: set up time
style.use('ggplot')
start = dt.datetime(2000,1,1)
end = dt.datetime(2019,7,28)
#Step 3: get the data by DataReader
df = web.DataReader('TSLA','yahoo',start,end)
df.head()
print(df.tail(6))
#Step 4: export the file to csv file
df.to_csv('tesla_price.csv')

#After completing a csv file which contains the data of Tesla stock price, we may import it and visualize our data.
df1 = pd.read_csv('tesla_price.csv',parse_dates=True,index_col=0)
df1.head() #check the data
#Plot the data
df1.plot() #df1[''].plot if we want to plot a specific column
plt.show()

#Manipiluate data and visualization
#Step 1: calculate the Moving Average of Adj Closing Price of 100 days.
#pd.DataFram.rolling() is to generate rolling window of calculation.

df1['100MA'] = df['Adj Close'].rolling(window = 100).mean()
#However, the first few rows don't have the calculation because the lack of data, so we can modify it by inplace.
df1.dropna(inplace=True)
print(df.head())
print(df.tail())

#Or we don't need to change the DataFrame
#df['100MA'] = df['Adj Close'].rolling(window = 100, min_periods = 0).mean()

#To draw the graph by subplot instead of plot.(Matplotlit only)
# define vertical and horizontal axis
axis1 = plt.subplot2grid((10,1),(0,0),5,1)
axis2 = plt.subplot2grid((10,1),(5,0),1,1,sharex=axis1)

axis1.plot(df1.index,df1['Adj Close'])
axis1.plot(df1.index,df1['100MA'])
axis2.plot(df1.index,df1['Volume'])
plt.show()

#Create Candlestick graph /OHLC graph (OHLC stands for open,high,low,close)
#Resample
#df_mean = df['Adj Close'].resample('10D').mean() #Avg value over 10 days.Every 10 days take a mean.
df_volume = df['Volume'].resample('10D').sum()
df_ohlc = df['Adj Close'].resample('10D').ohlc()

print(df_ohlc.head())
#print(df_mean)

#Because Candlestick requires the column of date as index, we need to modify it (Candlestick uses a different version of date)
df_ohlc.reset_index(inplace=True)
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

#Candlestick graph indicates the direction of going up or down of OHLC.
ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5,colspan=1)
ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1,colspan=1,sharex=ax1)
ax1.xaxis_date() #We need to convert it back to original date
candlestick_ohlc(ax1,df_ohlc.values,width=2,colorup='g')
#fill_between : fill the area between two horizontal curves
ax2.fill_between(df_volume.index.map(mdates.date2num),df_volume.values,0)
plt.show()






















