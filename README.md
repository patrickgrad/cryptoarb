# cryptoarb

[![Build Status](https://travis-ci.org/patrickgrad/cryptoarb.svg?branch=master)](https://travis-ci.org/patrickgrad/cryptoarb)

# Abstract

Pure arbitration strategy using several types of cryptocurrencies. 

This code looks for opportunites to trade based on the price of the same coin on two or more different exchanges. If the ask on one exchange is lower than the bid on another you can "guarantee" a profit. This strategy is semi-automatic: it automatically finds opportunities and presents a concise summary to the trader on the command line. The trader can then choose to execute the trade based on the summary presented.  

In the future this strategy will be fully automated.  

# Moving Forward

-Capitalizing on the largest opportunities first
-Transfering funds between exchanges/accounts in time to take advantage of opportunities 
-Finding path of least resistance(lowest cost) to get funds from one exchange to another.

# apiengine.py

This library is responsible for creating a universal API interface to easily communicate with external API services.  

# orderengine.py

Responsible for placing order, making sure balance is availible, plus some testing capabilities.  
