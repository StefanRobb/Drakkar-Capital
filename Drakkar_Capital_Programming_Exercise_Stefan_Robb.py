#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Drakkar Capital Pcap Project
# Stefan Robb - Revised: June 15th, 2020
# I, Stefan Robb, certify that this submission contains my own work, except as noted.


# In[3]:


import json
import csv
import time


# In[4]:


# converts abbreviated months into respective numerical value
def getMonth(month):
    return{
        'Jan' : '01',
        'Feb' : '02',
        'Mar' : '03',
        'Apr' : '04',
        'May' : '05',
        'Jun' : '06',
        'Jul' : '07',
        'Aug' : '08',
        'Sep' : '09', 
        'Oct' : '10',
        'Nov' : '11',
        'Dec' : '12'
    }[month]


# In[5]:


# left-pads the numerical date with 0 if <10
def getDate(date):
    date = date.replace(',','')
    if int(date) < 10:
        return str(date).zfill(2)
    else:
        return date


# In[6]:


# strip right last 3 digits and insert colon into time
def getTime(time):
    time = time[:15]
    return time[:8] + ':' + time[8:] 


# In[7]:


# hexadecimal to decimal conversion (little endian)
def hexToDec(hexstr):
    lehex = ''.join(reversed([hexstr[i:i+2] for i in range(0, len(hexstr), 2)]))
    decstr = str(int(lehex, 16))
    return decstr


# In[26]:


def main():  
    with open("markettradereports_20150909.json", "r") as read_file: # import trade report packets as a JSON file
        tradereports = json.load(read_file)
        
    with open('Trade_log_20150909.csv', 'w') as tradelog:
        trade_writer = csv.writer(tradelog, delimiter = ',')
        trade_writer.writerow(['Date', 'Local Time', 'Exchange Time', 'Symbol', 'Price', 'Volume', 'Buy Broker', 'Sell Broker', 'Delay'])   
        
        for tr in tradereports:
            datetime = tr.get('_source').get('layers').get('frame').get('frame.time')
            dtlist = datetime.split()

            date = dtlist[2] + getMonth(dtlist[0]) + getDate(dtlist[1]) # assuming YYYYMMDD (0909)
            localtime = getTime(dtlist[3])

            data = tr.get('_source').get('layers').get('data').get('data.data')
            datalist = data.split(':')

            exchgtime = hexToDec(''.join(datalist[82:90]))
            exchgtimeepoch = exchgtime[:len(exchgtime) - 6] + '.' + exchgtime[len(exchgtime) - 6:]
            exchgtime = time.strftime("%H:%M:%S:." + exchgtimeepoch[-6:], time.localtime(float(exchgtimeepoch)))

            symbol = bytes.fromhex(''.join(datalist[23:32])).decode('ASCII')

            price = hexToDec(''.join(datalist[36:44]))
            if len(price) < 6:
                price = '.0' + price[:len(price) - 3]
            else:
                price = price[:len(price) - 6] + '.' + price[len(price) - 6:len(price) - 3]

            volume = hexToDec(''.join(datalist[44:48]))

            buybroker = hexToDec(''.join(datalist[48:50]))
            sellbroker = hexToDec(''.join(datalist[62:64]))
            
            frametimeepoch = tr.get('_source').get('layers').get('frame').get('frame.time_epoch')
            delay = float(frametimeepoch) - float(exchgtimeepoch)

            trade_writer.writerow([date, localtime, exchgtime, symbol, price, volume, buybroker, sellbroker, delay])


# In[27]:


if __name__ == "__main__":
    main()


# In[ ]:




