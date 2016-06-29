from __future__ import print_function

import statuses as s
import apiengine
import orderengine

import colorama
from colorama import Fore, Back, Style

import os
import sys
import time
import random
import urllib2

def run(context,currencies):
    exchanges = apiengine.get_books(context,currencies,0,21) 

    for i in range(len(exchanges)):
        name1 = context[i].__class__.__name__
        for ii in range(len(exchanges)):
            name2 = context[ii].__class__.__name__
            if(i != ii):
                for currency in range(len(currencies)):
                    bids_i = exchanges[i][currency][0]
                    bids_i_top = bids_i[0]
                    
                    asks_ii = exchanges[ii][currency][1]
                    asks_ii_top = asks_ii[0]
                    
                    #if we aren't comparing to the same exchange and the bid > ask, we can then buy at the ask and sell at the bid
                    if s.DEBUG_PRINT == 1:
                        print(str(bids_i_top[0]) + ">" + str(asks_ii_top[0]))
                        print(float(bids_i_top[0]) > float(asks_ii_top[0]))
                    if(float(bids_i_top[0]) > float(asks_ii_top[0])):
                        squat((context[i],context[ii]),(bids_i,asks_ii),currencies[currency])

#this is the function that gets called once an opportunity is detected
#Process:
#    1. First see how deep in the book the opportunity exists.
#    2. Take the availible and profitable trades if they yield at least $0.01
#        A trade consists of selling a currency on one market and buying on another and immediatly sending the
#        purchased currency to the account we just sold out of. Transfer some coin with a good reverse conversion 
#        rate to the buying account and convert to the original coin.
#    3. Make sure there are sufficient funds to execute trades, if not, just partially execute
#    4. Start making orders that are very slightly cheaper than the ask and slightly more expensive than the bid
#        in an effort to hold onto the opportunity. 
#    5. Stop doing this once orders take longer than two minutes to execute.
def squat(context,data,currency):
        
    bids_i = data[0]
    asks_ii = data[1]
    api_i = context[0]
    api_ii = context[1]

    fee_i = .0000
    fee_ii = .0000
    
    i = 0
    ii = 0
    a = 1
    
    #1 & 2.
    #very simple profitability algo
        #increment bid, if profitability incresed keep the change, if it didn't dont keep the change
        #increment bid, if profitability incresed keep the change, if it didn't dont keep the change
        #keep going as long as a change was made

    #calc baseline profit

    if float(bids_i[i][1]) > float(asks_ii[ii][1]):
        volume = float(asks_ii[ii][1])
    else:
        volume = float(bids_i[i][1])

    c = float(bids_i[i][0])*volume
    cc = float(asks_ii[ii][0])*volume
    profit = c-cc

    max_buy_vol = float(asks_ii[ii][1])
    max_sell_vol = float(bids_i[i][1])

    while a == 1 and i<len(bids_i)-1 and ii<len(asks_ii)-1:
        a=0

        if float(bids_i[i+1][1]) > float(asks_ii[ii][1]):
            volume = float(asks_ii[ii][1])
        else:
            volume = float(bids_i[i+1][1])

        c = float(bids_i[i+1][0])*volume
        cc = float(asks_ii[ii][0])*volume

        profit_new = profit + c-cc
        if(profit_new > profit):
            i += 1
            profit = profit_new
            a = 1
            max_sell_vol += float(bids_i[i][1])


        if float(bids_i[i][1]) > float(asks_ii[ii+1][1]):
            volume = float(asks_ii[ii+1][1])
        else:
            volume = float(bids_i[i][1])

        c = float(bids_i[i][0])*volume
        cc = float(asks_ii[ii+1][0])*volume

        profit_new = profit + c-cc
        if(profit_new > profit):
            ii += 1
            profit = profit_new
            a = 1
            max_buy_vol += float(asks_ii[ii][1])

    #now figure out what's actually going to happen
    #first find the actual volume we'll be using

    if max_sell_vol<max_buy_vol:
        target_vol = max_sell_vol
    else:
        target_vol = max_buy_vol

    profit = 0      #reset profit here to get real calculation
    i_r = 0         #r means revised caus that's what were about to do
    ii_r = 0
    i_vol = 0
    ii_vol = 0

    i_end = 0
    ii_end = 0

    #we need to make sure that all the trades we're making are still profitable at the new volume
    #factor in the fees

    while i_r <= i:
        if (i_vol + float(bids_i[i_r][1])) <= target_vol:
            if s.DEBUG_PRINT == 2:
                print("i_vol=" + str(i_vol))
            i_vol += float(bids_i[i_r][1])
            profit += (float(bids_i[i_r][0])*float(bids_i[i_r][1]))-(float(bids_i[i_r][0])*float(bids_i[i_r][1]*fee_i))
            if s.DEBUG_PRINT == 2:
                print(profit)
            i_r += 1        
        else:
            i_end = target_vol - i_vol
            i_vol += i_end
            profit += (float(bids_i[i_r][0])*i_end)-(float(bids_i[i_r][0])*i_end*fee_i)
            break

    while ii_r <= ii:
        if (ii_vol + float(asks_ii[ii_r][1])) <= target_vol:
            if s.DEBUG_PRINT == 2:
                print("ii_vol=" + str(ii_vol))
            ii_vol += float(asks_ii[ii_r][1])
            profit -= (float(asks_ii[ii_r][0])*float(asks_ii[ii_r][1]))+(float(asks_ii[ii_r][0])*float(asks_ii[ii_r][1]*fee_ii))
            if s.DEBUG_PRINT == 2:
                print(profit)
            ii_r += 1        
        else:
            ii_end = target_vol - ii_vol
            ii_vol += ii_end
            profit -= (float(asks_ii[ii_r][0])*ii_end)+(float(asks_ii[ii_r][0])*ii_end*fee_ii)
            break

    if s.DEBUG_PRINT == 1:
        print(str(bids_i[i_r][0]) + ">" + str(asks_ii[ii_r][0]))
    if s.DEBUG_PRINT == 2:
        print("DEPTH OLD: " + "Bids=" + str(i) + " Asks=" + str(ii))
    if s.DEBUG_PRINT == 1:
        print("DEPTH: " + "Bids=" + str(i_r) + " Asks=" + str(ii_r))
        print(bids_i)
        print(asks_ii)

        print("target_vol=" + str(target_vol))
        print("i_vol=" + str(i_vol))
        print("ii_vol=" + str(ii_vol))

        print("PROFIT: " + str(profit) + currency[1])

    if profit > 0.01 or (profit > 0 and profit/(target_vol*(float(bids_i[i_r][0])*float(asks_ii[ii_r][0])*0.5))>10):
        print(s.TRADE_BUY + "BUY: " + str(ii_vol) + " " + currency[0] + " on " + api_ii.__class__.__name__  + " @ " + str(asks_ii[ii_r][0]) + "-" + str(asks_ii[0][0]))
        print(s.TRADE_SELL + "SELL: " + str(i_vol) + " " + currency[0] + " on " + api_i.__class__.__name__ + " @ " + str(bids_i[0][0]) + "-" + str(bids_i[i_r][0]))
        print(s.PROFIT + "MAX PROFIT: " + str(profit) + " " + currency[1])
        print(s.TRADE_WITHDRAW + "Send " + str(target_vol) + " " + currency[0] + " from " + api_i.__class__.__name__ + " to " + api_ii.__class__.__name__)
        
        while True:
            ss = raw_input('Type [y] to initiate trade, [n] to cancel: ')

            if ss == "y":
                print(s.TRADE + "Trade initiated...")
                for b in range(i_r):
                    orderengine.sell(api_i,currency,bids_i[b][0],bids_i[b][1])
                    if b > 6:       #need to make sure we don't get kicked off the apis
                        time.sleep(0.5)

                    
                for c in range(ii_r):
                    orderengine.buy(api_ii,currency,asks_ii[c][0],asks_ii[c][1])
                    if c > 6:       #need to make sure we don't get kicked off the apis
                        time.sleep(0.5)

                orderengine.sell(api_i,currency,bids_i[i_r][0],i_end)
                orderengine.buy(api_ii,currency,asks_ii[ii_r][0],ii_end)
                time.sleep(2) #wait a hot sec, at this point we aren't really in a rush, gotta let the apis cool down

                #need to now transfer i_vol worth of currency[0] to api_i from api_ii
                orderengine.withdraw(api_ii,currency[0],i_vol,apiengine.ADDRESSES[api_i.INDEX])

                time.sleep(1) #wait some more

                apiengine.BALANCE = apiengine.get_balance(apiengine.CONTEXT,apiengine.CURRENCIES)
                break
            elif ss == "n":
                print(s.TRADE + "Trade canceled.")
                break

def main():
    context = apiengine.CONTEXT
    currencies = apiengine.CURRENCIES
    balance = apiengine.BALANCE
    print(s.RUNNING + "Operating using " + str(len(currencies)) + " currency combinations")
    addresses = apiengine.ADDRESSES

    i = 0
    print("")
    while(i<10):
        chars = ["-", "\\" , "|", "/"]
        
        try:
            run(context,currencies)
        except urllib2.HTTPError:
            print(s.ERROR + "CONNECTION REFUSED")
                
        time.sleep(1)
        print(chars[i%(len(chars))])
        sys.stdout.write('\x1b[1A')   #go back up a line, makes a cool "loading" animation
        i = i + 1
    
if __name__ == '__main__':
    main()




