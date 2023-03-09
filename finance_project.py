# -*- coding: utf-8 -*-
"""Finance Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jw4xgT3Kedf9qsz1Z-OLQtQYvUiLZQUZ

# Finance Data Project 

In this data project I have focused on exploratory data analysis of bank stock prices and see how they progressed throughout the financial crisis all the way to early 2016..
____

## Get the Data
Used pandas datareader to directly read data from Yahoo finance
"""

!pip install --upgrade pandas-datareader

# Commented out IPython magic to ensure Python compatibility.
from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
# %matplotlib inline

"""## Data

We got stock information for the following banks from Jan 1st 2006 to Jan 1st 2016:
*  Bank of America
* CitiGroup
* Goldman Sachs
* JPMorgan Chase
* Morgan Stanley
* Wells Fargo

"""

start = datetime.datetime(2006, 1, 1)
end = datetime.datetime(2016, 1, 1)

# Bank of America
BAC = data.DataReader("BAC", 'yahoo', start, end)

# CitiGroup
C = data.DataReader("C", 'yahoo', start, end)

# Goldman Sachs
GS = data.DataReader("GS", 'yahoo', start, end)

# JPMorgan Chase
JPM = data.DataReader("JPM", 'yahoo', start, end)

# Morgan Stanley
MS = data.DataReader("MS", 'yahoo', start, end)

# Wells Fargo
WFC = data.DataReader("WFC", 'yahoo', start, end)

"""**Created a list of the ticker symbols (as strings) called tickers**"""

tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']

"""**Used pd.concat to concatenate the bank dataframes together to a single data frame called bank_stocks.**"""

bank_stocks = pd.concat([BAC, C, GS, JPM, MS, WFC],axis=1,keys=tickers)

"""**Named the column levels**"""

bank_stocks.columns.names = ['Bank Ticker','Stock Info']

"""** Check the head of the bank_stocks dataframe.**"""

bank_stocks.head()

"""# Exploratory Data Analysis (EDA)

Let's explore the data!
Let's find the max Close price for each bank's stock throughout the time period
"""

bank_stocks.xs(key='Close',axis=1,level='Stock Info').max()

"""**Created a new empty DataFrame called returns containing the returns for each bank's stock**"""

returns = pd.DataFrame()

for tick in tickers:
    returns[tick+' Return'] = bank_stocks[tick]['Close'].pct_change()
returns.head()

"""**Generated a pairplot using seaborn of the returns dataframe.**"""

import seaborn as sns
sns.pairplot(returns[1:])

"""**Found on what dates each bank stock had the best and worst single day returns. 4 out of the 6 banks share the same day for the worst drop, that is on Inauguration Day of Barack Obama**"""

# Worst Single Day Gain
returns.idxmin()

# Best Single Day Gain
returns.idxmax()

"""**Calculated the standard deviation of the returns, to figure out the riskiest stocks**"""

returns.std() # Citigroup riskiest

"""**Found the Standard Deviations for the year 2015**"""

returns.ix['2015-01-01':'2015-12-31'].std() # Very similar risk profiles, but Morgan Stanley or BofA

"""**Generated a distplot using seaborn of the 2015 returns for Morgan Stanley**"""

sns.distplot(returns.ix['2015-01-01':'2015-12-31']['MS Return'],color='green',bins=100)

"""**Generated a distplot using seaborn of the 2008 returns for CitiGroup**"""

sns.distplot(returns.ix['2008-01-01':'2008-12-31']['C Return'],color='red',bins=100)

"""____
#  Visualizations
### Imports
"""

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
# %matplotlib inline

import plotly

"""**Generated a line plot showing Close price for each bank for the entire index of time.**"""

for tick in tickers:
    bank_stocks[tick]['Close'].plot(figsize=(12,4),label=tick)
plt.legend()

bank_stocks.xs(key='Close',axis=1,level='Stock Info').plot()

"""## Moving Averages

Let's analyze the moving averages for these stocks in the year 2008. 

**Plot the rolling 30 day average against the Close Price for Bank Of America's stock for the year 2008**
"""

plt.figure(figsize=(12,6))
BAC['Close'].ix['2008-01-01':'2009-01-01'].rolling(window=30).mean().plot(label='30 Day Avg')
BAC['Close'].ix['2008-01-01':'2009-01-01'].plot(label='BAC CLOSE')
plt.legend()

"""**Generated a heatmap of the correlation between the stocks Close Price**"""

sns.heatmap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)

"""**Used seaborn's clustermap to cluster the correlations together**"""

sns.clustermap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)

"""# The End!


"""