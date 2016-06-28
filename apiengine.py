import poloniex as pol
import cexapi as cex

import statuses as s

def start_apis():
    capi = cex.cex('up100456121','jnDM4Y9rlBdSfiOZbDSNuvWi6EY','HCmNumFRlaK6FrY1hIyLvvTqwso')
    capi.INDEX = 0
    if(capi.balance().has_key('username')):
        print(s.SUCCESS + "Connected to CEX.io")
    else:
        print(s.ERROR + "Unable to connected to CEX.io")
    
    papi = pol.poloniex('FWL8QZNC-B9PGT6V9-447WKQ8Z-7KIF5EHA','02ac097cbdad60947f0918141d95365d8b23d16bff02ab605cb061182b5b9a5427aa49f825445e59c019e43c6a9ea29d40d6a376d5dca923f86e3b6dd5396a7b')
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
    return [("BTC","USD"),("LTC","USD"),("ETH","USD"),("ETH","BTC"),("LTC","BTC")]

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
                #print(call)
                addrs = []
                for curr in currencies:
                    for x in curr:
                        if(x != "USD"):
                            for y,data in call.iteritems():
                                #print(x + " " + y)
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
            #print("CEX.io book: ")
            #print(b)
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


#TODO: highest priority right here
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
