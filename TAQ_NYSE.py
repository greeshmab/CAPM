##############################################
# Some Tech terms
# Consolidated Tape Association (CTA) Plan, 
# Unlisted Trading Privileges (UTP) Plan
#
#
#
# Assumptions made:
# The data for each stock is even wrt timings
# and the timestamps are in ascending order 
# The returns odtained just by R(i)-R(i-1)  
#
#############################################
import gzip
import pandas as pd
import os,sys
from scipy import stats
import numpy as np

with gzip.open('/content/drive/My Drive/EQY_US_ALL_TRADE_20161026.gz', 'r') as f:
#with gzip.open('/content/drive/My Drive/tempData.rtf.gz', 'r') as f:
    fileContent = f.readlines()

print('no. of rows are : ', len(fileContent), '\n')

#Create a dictionary with key as the symbol and the value 
#is dictionary of trades for the symbol with key as tradeID
data = {}

#remove first and last lines of the file
fileContent = fileContent[1:-1]

for line in fileContent:
    #Convert byte obj to string
    lineData = "".join( chr(x) for x in line)
    temp = lineData.split('|')
    if(len(temp) < 15):
      continue;
    if(temp[1]=='Exchange'):
      continue;
      
    if(temp[0]=='END'):
      continue;
      
    #print(temp)
    
    time = temp[0]
    sym =  temp[2]
    trade = {}
    trade['time'] = temp[0]
    try:
        trade['price'] = float(temp[5])
        trade['volume'] = float(temp[4])
    except ValueError:
        print ("error on line ",line)
   
    #Check if there is dict for this symbol
    if sym not in data:
      data[sym] = []
    
    #append this trade to the symbol list
    data[sym].append(trade)
    
    
print("The total number of Stocks Traded are : ", len(data), "\n")


#Avg price, min price, max proce, open price and close price for each stock
#loop through data dictionary and for each key i.e stock, get the values

metrics = {}

for key,value in data.items():
  temp = value
  size = len(temp)
  #print(size)
  metric = {}
  
  metric['openPrice'] = temp[0]['price']
  metric['closePrice'] = temp[size-1]['price']
  avg = temp[0]['price'] 
  minimum = temp[0]['price'] 
  maximum = temp[0]['price']
  for i in range(1,size):
    price = temp[i]['price']
    avg = avg + price
    
    if(price < min):
      minimum = price 
    if(price > max):
      maximum = price
  metric['average'] = avg/size
  metric['minimum'] = minimum
  metric['maximum'] = maximum
  metric['Entries'] = size
  
  metrics[key] = metric 
  
print(metrics)

#Get returns and calculate correlation factor with the market 
#
#df = pd.DataFrame.from_dict(data)
#print(df)

