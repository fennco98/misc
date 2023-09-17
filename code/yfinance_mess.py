#Import modules
import os
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime
import scipy

#Import Ticker information from YF
#allows calling various functions against given object(?)
VOO_inf = yf.Ticker('VOO')
VGT_inf = yf.Ticker('VGT')
GBMINT_inf = yf.Ticker('GBMINTBO.MX')


#Import Ticker data from YF
VOO = yf.download('VOO')
VGT = yf.download('VGT')
GBMINT = yf.download('GBMINTBO.MX')

# --------------------------------------------------------------------------------------------

##Import Data
# print('Short Name:')
# print(VOO_inf.info['shortName'])
# print('Symbol:')
# print(VOO_inf.info['symbol'])
# print('-----------------------------------------------------------------------------------\n')

df_VOO = pd.DataFrame(VOO['Close'])

def mins_or_maxes(df, mins_or_maxes, period=90):
## pass dataframe with data of note as .values; select 'mins' or 'maxes',
# and specify peridod (in days)
# for some reason, can only call once on a df with .values; cant do maxes and mins

    if mins_or_maxes == 'mins':
        #get the indicies mins of values in given df, as an array
        mins = scipy.signal.argrelextrema(df_VOO.values, np.less_equal, order=period)[0]
        #drop these values into a new column in the same df 
        df['mins'] = df.iloc[mins]

    elif mins_or_maxes == 'maxes':
        maxes = scipy.signal.argrelextrema(df_VOO.values, np.greater_equal, order=period)[0]
        df['maxes'] = df.iloc[maxes]

mins_or_maxes(df_VOO, 'maxes', period=90)
#mins_or_maxes(df_VOO, 'maxes', period=90)

plt.style.use('dark_background')

fig, ax = plt.subplots(nrows=1, ncols=2, sharex=True, figsize=(15,5))

ax[0].set_title('VOO Close', fontsize=15)
ax[0].plot(VOO['Close'], color='g', linewidth=1)
#ax[0].scatter(df_VOO['mins'].index, df_VOO['mins'], color='r')
ax[0].scatter(df_VOO['maxes'].index, df_VOO['maxes'], color='b')
ax[0].set_xlabel('Date')
ax[0].set_ylabel('Share Price at Close [USD]')

ax[1].set_title('VOO Volume', fontsize=15)
ax[1].plot(VOO['Volume'], color='g', linewidth=1)
ax[1].set_xlabel('Date')
ax[1].set_ylabel('Whole Shares Traded per Day [USD]')

# plt.savefig('GEN_YTD_VOO.png',bbox_inches='tight',dpi=100)
plt.show()

print('------------------------------------------------------------------------------------\n')

#Compute 10 day returns
# VOO = pd.DataFrame(VOO)
# VOO['Returns'] = VOO['Close'].pct_change()
# print(VOO.tail(10))
# print('------------------------------------------------------------------------------------\n')