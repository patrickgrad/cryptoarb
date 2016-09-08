import csv
import poloniex as pol
import cexapi as cex

import statuses as s

def start_apis():
    keys = {}
    with open('keys.csv', 'rb') as csvfile:
        r = csv.reader(csvfile)
        i = 0
        a = []
        for row in r:
            if i == 0:
                a = row
            else:
                keys[row[0]] = {}
                dic = keys[row[0]]
                for col in range(1,len(row)):
                    if col != "":
                        dic[a[col]] = row[col]
            i += 1

    c = keys["cex"]
    capi = cex.cex(c["username"],c["public key"],c["private key"])
    capi.INDEX = 0
    if(capi.balance().has_key('username')):
        print(s.SUCCESS + "Connected to CEX.io")
    else:
        print(s.ERROR + "Unable to connected to CEX.io")
    
    p = keys["poloniex"]
    papi = pol.poloniex(p["public key"],p["private key"])
    papi.INDEX = 1
    if(papi.returnBalances().has_key('BTC')):
        print(s.SUCCESS + "Connected to Poloniex")
    else:
        print(s.ERROR + "Unable to connected to Poloniex")
        
    context = (capi,papi)
    
    return context

CONTEXT = start_apis()

def get_currencies(context):
    #TODO: would like for this to work automatically some day           
    return [("BTC","USD"),("LTC","USD"),("ETH","USD")]

CURRENCIES = get_currencies(CONTEXT)

def get_balance(context,currencies):
    balance = []
    for x in range(len(context)):
        name = context[x].__class__.__name__
        api = context[x]

        if(name == 'cex'): #CEX.io api
        	bal = api.balance()
        	for c in currencies:
	            if(float(bal[c[0]]['available']) < 0.2 and c[1] == "USD"):
	                print(s.WARNING + "Cex.io: Low " + c[0] + " balance")
	            balance.append(bal)

        elif(name == 'poloniex'): #Poloniex api
        	bal = api.api_query('returnCompleteBalances')
	        for c in currencies:
	            if(float(bal[c[0]]['available']) < 0.2 and c[1] == "USD"):
	                print(s.WARNING + "Poloniex: Low " + c[0] + " balance")
	            balance.append(bal)
            
    return balance

BALANCE = get_balance(CONTEXT,CURRENCIES)

def get_addresses(context, currencies):
    addresses = []
    for x in range(len(context)):
            name = context[x].__class__.__name__
            api = context[x]

            if(name == 'cex'): #CEX.io api
                addrs = []
                for curr in currencies:
                    for x in curr:
                        if(x != "USD"):
                            addr = api.api_call('get_address', {"currency":x}, 1)
                            if(addr['ok'] == 'ok'):
                                addrs.append((x,addr['data']))
                            else:
                                print(s.ERROR + "CEX.io - " + "Currency \"" + x + "\" expected but no address found")
                addresses.append(addrs)

            elif(name == 'poloniex'): #Poloniex api
                call = api.api_query('returnDepositAddresses')
                addrs = []
                for curr in currencies:
                    for x in curr:
                        if(x != "USD"):
                            for y,data in call.iteritems():
                                if(x==y):
                                    addrs.append((y,data))
                addresses.append(addrs)

    return addresses

ADDRESSES = get_addresses(CONTEXT,CURRENCIES)

def get_books(context,currencies,start,end): #start is inclusive, end is exclusive
    books = []
    for x in range(len(context)):
        name = context[x].__class__.__name__
        api = context[x]
        if(name == 'cex'): #CEX.io api
            b = []
            for curr in currencies:
                book = api.order_book(curr[0] + "/" + curr[1])
                if(book.has_key("error")):
                    print(s.ERROR + book["error"] + " Order: " + curr[0] + "/" + curr[1])
                else:
                    bok = (book['bids'][start:end][start:end],book['asks'][start:end][start:end])
                b.append(bok)
            books.append(b)

        elif(name == 'poloniex'): #Poloniex api
            b = []
            for curr in currencies:
                c = curr[1]
                if(curr[1] == "USD"):
                    c = c + "T"
                book = api.returnOrderBook(c + "_" + curr[0])
                if(book.has_key("error")):
                    print(s.ERROR + book["error"] + " Order: " + c + "_" + curr[0])
                else:
                    bok = (book['bids'][start:end][start:end],book['asks'][start:end][start:end])
                b.append(bok)
            books.append(b)
    return books


#TODO: get the real fees
def get_fees(context):
    fees = []
    for x in range(len(context)):
            name = context[x].__class__.__name__
            api = context[x]

            if(name == 'cex'): #CEX.io api
                f = []
                fees.append(f)

            elif(name == 'poloniex'): #Poloniex api
                f = []
                fees.append(f)

    return fees

FEES = get_fees(CONTEXT)
