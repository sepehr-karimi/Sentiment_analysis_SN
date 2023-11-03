from ctypes import sizeof
import pandas as pd
import numpy as np
import mplfinance as fplt
# import required packages
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpdates
import yfinance as yf
#import talib as ta


# Name of the Stock
ticker_name = "shghadir"
#Reading social DataFrame , columns=['date', 'total views', 'total posts', 'imp. views']
Social_data = pd.read_csv("C:\\Users\\Sepehr\\Desktop\\SN_Project_final\\3_Data_for_ML_Plot_withImportance\\shghadir_social.csv")

#Reading Financial Dataframe, columns=[Date,open,high,low,volume]
data = pd.read_csv("C:\\Users\\Sepehr\Desktop\\SN_Project_final\\3_Data_for_ML_Plot_withImportance\\shghadir_financial.csv")

#Reading indicator raw data
social_indicator = pd.read_csv("C:\\Users\\Sepehr\\Desktop\\SN_Project_final\\4_Results_ML\\shghadir_indicator_both.csv")

#getting indexed done
social_data_edited =  Social_data[Social_data.date.isin(data.date)] 
financial_data_edited =  data[data.date.isin(social_data_edited.date)] 
social_indicator =  social_indicator[social_indicator.date.isin(Social_data.date)]
raw_data_frame = pd.DataFrame(financial_data_edited, columns=['date','open', 'high', 'low', 'close','volume'])
raw_data_frame['date'] = pd.to_datetime(raw_data_frame['date'],yearfirst=True,format="%Y%m%d")
social_data_edited['date'] = pd.to_datetime(social_data_edited['date'],yearfirst=True,format="%Y%m%d")   
social_indicator['date'] = pd.to_datetime(social_indicator['date'],yearfirst=True,format="%Y%m%d")   

#setting indexes
indexed_FDF = raw_data_frame.set_index('date')
indexed_SDE = social_data_edited.set_index('date')
indexed_SI = social_indicator.set_index('date')

#Setting time of plotting
Plot_date_begin = '2020-10-02'
Plot_date_end = '2022-01-29'
indexed_FDF = indexed_FDF.loc[Plot_date_begin:Plot_date_end,:]
indexed_SDE = indexed_SDE.loc[Plot_date_begin:Plot_date_end,:]

#merging all in one Dataframe
indexed_SI = indexed_SI.merge(indexed_FDF, on='date')
indexed_SI = indexed_SI.merge(indexed_SDE, on='date')
print(indexed_SI)
#Creating Social signal for plot
signal   = []
previous = 2
pre_previous = 2
for date,value in indexed_SI['Predicted'].iteritems():
      s = indexed_SI['close'][date] * 0.98
      s = s.item()
      if (value == 1) :
            #& (previous == 1)&(pre_previous == 1)
            signal.append(s)
      else:
            signal.append(np.nan)
      pre_previous =  previous     
      previous = value

apds = [fplt.make_addplot(indexed_SI['close'],linestyle='dashdot'),
        fplt.make_addplot(signal,type='scatter',markersize=100,marker='^'),
        fplt.make_addplot((indexed_SI['imp. views'].rolling(15).mean()),color='b',linestyle='dotted')
       ]

fplt.plot(indexed_SI,type='line',figscale=1.1,volume=True,style='yahoo',addplot=apds,title=f"\n{ticker_name} social & financial analysis",mav=(5,20), ylabel='Data', ylabel_lower='Volume')
#savefig='img.png'







