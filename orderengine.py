import apiengine
import statuses as s

#implements controls on ordering and moving funds as well as logs transactions

ORDERS = []
RATIO = {"MARGIN":.2,"CASH":.4,"COIN":.4} #margin here is loaning out money, not taking it out


def withdraw(api,currency,volume,address):
	#for api, withdraw amount of currency to address
	if apiengine.BALANCE[api.INDEX].has_key(currency) and float(apiengine.BALANCE[api.INDEX][currency]['available']) >= volume:
		#we're good to move the funds
		apiengine.BALANCE[api.INDEX][currency]['available'] = float(apiengine.BALANCE[api.INDEX][currency]['available']) - volume

		r=w_help(api,currency,volume,address)
		if type(r) == bool:
			print(s.SUCCESS + "Initiated transfer of " + str(volume) + currency)
			print("ADDRESS: " + str(address))
			return True
		else:
			print(s.ERROR + r)
			return False

	elif float(apiengine.BALANCE[api.INDEX][currency]['available']) > 0.015:
		vol_new = float(apiengine.BALANCE[api.INDEX][currency]['available'])
		print(s.FUNDWAR + "Not enough funds to withdraw " + str(volume) + currency + ". Partial withdraw using " + str(vol_new) + currency)

		r=w_help(api,currency,vol_new,address)
		if type(r) == bool:
			print(s.SUCCESS + "Initiated transfer of " + str(vol_new) + currency)
			print("ADDRESS: " + str(address))
			return True
		else:
			print(s.ERROR + r)
			return False

	else:
		print(s.FUNDERR + "Cannot complete transfer, no " + currency + " availible in " + api.__class__.__name__)
		return False


def w_help(api,currency,volume,address):
	name = api.__class__.__name__

	if s.DEBUG == 1: #debug mode, everything works unless we say it doesn't
		if s.DEBUG_ERROR_WITHDRAW == -1:
			return True
		else:
			return s.DEBUG_ERROR_WITHDRAW 

	if s.DEBUG == 2: #logging mode, sort of like paper trading
		if s.DEBUG_ERROR_WITHDRAW == -1:
			return True
		else:
			return s.DEBUG_ERROR_WITHDRAW

	if s.DEBUG == 0: #live fire, do not point at faces
		if(name == "cex"):
				return "Cannot transfer out of cex at this time"

		if(name == "poloniex"):
			result = api.withdraw(currency,volume,address)
			if result.has_key("error"):
				if s.DEBUG_PRINT == 1:
					print(result)
				return result["error"]
			else:
				return True



def buy(api,pair,price,volume):
	#buy currency using the provided api
	
	if apiengine.BALANCE[api.INDEX].has_key(pair[1]) and float(apiengine.BALANCE[api.INDEX][pair[1]]['available']) >= volume:
		#we have enough to buy what we want
		apiengine.BALANCE[api.INDEX][pair[1]]['available'] = float(apiengine.BALANCE[api.INDEX][pair[1]]['available']) - volume

		r=b_help(api,pair,price,volume)
		if type(r) == bool:
			print(s.TRADE_BUY + "BUY: " + str(volume) + " " + pair[0] + " @ " + str(price) + " " + pair[1] + " TOTAL: " + str(float(price)*float(volume)) + pair[1])
			return True
		else:
			print(s.ERROR + r)
			return False

	elif apiengine.BALANCE[api.INDEX].has_key(pair[1]) and float(apiengine.BALANCE[api.INDEX][pair[1]]['available']) > 0.001:
		vol_new = float(apiengine.BALANCE[api.INDEX][pair[1]]['available'])
		print(s.FUNDWAR + "Not enough funds to buy " + volume + pair[0] + ". Placing partial order for " + str(vol_new) + pair[0])

		r=b_help(api,pair,price,volume)
		if type(r) == bool:
			print(s.TRADE_BUY + "BUY: " + str(vol_new) + " " + pair[0] + " @ " + str(price) + " " + pair[1] + " TOTAL: " + str(float(price)*vol_new) + pair[1])
			return True
		else:
			print(s.ERROR + r)
			return False

	else:
		print(s.FUNDERR + "Cannot initiate trade, no " + pair[1] + " availible in " + api.__class__.__name__)
		return False

def b_help(api,pair,price,volume):
	name = api.__class__.__name__

	if s.DEBUG == 1: #debug mode, everything works unless we say it doesn't
		if s.DEBUG_ERROR_BUY == -1:
			return True
		else:
			return s.DEBUG_ERROR_BUY 

	#if s.DEBUG == 2: #logging mode, sort of like paper trading

	if s.DEBUG == 0: #live fire, do not point at faces
		if(name == "cex"):
			result = api.place_order('buy',volume,price,pair[0] + "/" + pair[1])
			if(result.has_key("id")):
				return True
			else:
				if s.DEBUG_PRINT == 1:
					print(result)
				return result["e"]

		if(name == "poloniex"):
			if pair[1] == "USD":
				c = pair[1] + "T"
			else:
				c = pair[1]
			result = api.buy(c + "_" + pair[0] ,price,volume)
			if result.has_key("error"):
				if s.DEBUG_PRINT == 1:
					print(result)
				return result["error"]
			else:
				return True

#TODO
def sell(api,pair,price,volume):
	#sell currency using the provided api
	
	if apiengine.BALANCE[api.INDEX].has_key(pair[0]) and float(apiengine.BALANCE[api.INDEX][pair[0]]['available']) >= volume:
		#we have enough to sell what we want
		apiengine.BALANCE[api.INDEX][pair[0]]['available'] = float(apiengine.BALANCE[api.INDEX][pair[0]]['available']) - volume

		r=s_help(api,pair,price,volume)
		if type(r) == bool:
			print(price)
			print(volume)
			print(s.TRADE_SELL + "SELL: " + str(volume) + " " + pair[0] + " @ " + str(price) + " " + pair[1] + " TOTAL: " + str(float(price)*float(volume)) + pair[1])
			return True
		else:
			print(s.ERROR + r)
			return False

	elif apiengine.BALANCE[api.INDEX].has_key(pair[0]) and float(apiengine.BALANCE[api.INDEX][pair[0]]['available']) > 0.001:
		vol_new = float(apiengine.BALANCE[api.INDEX][pair[0]]['available'])
		print(s.FUNDWAR + "Not enough funds to sell " + str(volume) + pair[0] + ". Placing partial order for " + str(vol_new) + pair[0])

		r=s_help(api,pair,price,vol_new)
		if type(r) == bool:
			print(price)
			print(volume)
			print(s.TRADE_SELL + "SELL: " + str(vol_new) + " " + pair[0] + " @ " + str(price) + " " + pair[1] + " TOTAL: " + str(float(price)*vol_new) + pair[1])
			return True
		else:
			print(s.ERROR + r)
			return False

	else:
		print(s.FUNDERR + "Cannot initiate trade, no " + pair[0] + " availible in " + api.__class__.__name__)
		return False

def s_help(api,pair,price,volume):
	name = api.__class__.__name__

	if s.DEBUG == 1: #debug mode, everything works unless we say it doesn't
		if s.DEBUG_ERROR_SELL == -1:
			return True
		else:
			return s.DEBUG_ERROR_SELL 

	#if s.DEBUG == 2: #logging mode, sort of like paper trading

	if s.DEBUG == 0: #live fire, do not point at faces
		if(name == "cex"):
			result = api.place_order('sell',volume,price,pair[0] + "/" + pair[1])
			if(result.has_key("id")):
				return True
			else:
				if s.DEBUG_PRINT == 1:
					print(result)
				return result["e"]

		if(name == "poloniex"):
			if pair[1] == "USD":
				c = pair[1] + "T"
			else:
				c = pair[1]
			result = api.sell(c + "_" + pair[0],price,volume)
			if result.has_key("error"):
				if s.DEBUG_PRINT == 1:
					print(result)
				return result["error"]
			else:
				return True