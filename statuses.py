import colorama
from colorama import Fore, Back, Style
import sys

DEBUG = 1   #set to 1 to enable debug mode, set to 0 to turn on regular trading, set to 2 for sandbox logging
DEBUG_PRINT = 0 #set to 1 to print off a lot of extra info, set to 2 to print off even more info, set to 0 to turn off
DEBUG_ERROR_BUY = -1 #set this to something to some string to test the exchange error handling or to -1 to not test the error handling
DEBUG_ERROR_SELL = -1 
DEBUG_ERROR_WITHDRAW = -1 


ERROR = "[ " + Fore.RED + "ERROR" + Fore.WHITE + " ] : "
SUCCESS = "[ " + Fore.GREEN + "SUCCESS" + Fore.WHITE + " ] : "
RUNNING = "[ " + Fore.GREEN + "RUNNING" + Fore.WHITE + " ] : "
WARNING = "[ " + Fore.YELLOW + "WARNING" + Fore.WHITE + " ] : "
FUNDWAR = "[ " + Fore.YELLOW + "LOW FUNDS" + Fore.WHITE + " ] : "
FUNDERR = "[ " + Fore.RED + "NO FUNDS" + Fore.WHITE + " ] : "
TRADE = Back.BLACK + "[ " + Fore.CYAN + "TRADE" + Fore.WHITE + " ] : "
TRADE_BUY = Back.BLACK + "[ " + Fore.GREEN + "BUY" + Fore.WHITE + " ] : "
TRADE_SELL = Back.BLACK + "[ " + Fore.RED + "SELL" + Fore.WHITE + " ] : "
TRADE_WITHDRAW = Back.BLACK + "[ " + Fore.MAGENTA + "TRANSFER" + Fore.WHITE + " ] : "
PROFIT = "[ " + Fore.GREEN + "PROFIT" + Fore.WHITE + " ] : "

def versioning():
    if('2.7.' in sys.version):
        print(SUCCESS + 'Python ' + sys.version)
    else:
        print(ERROR + 'Python version 2.7.xx required')
        return False

    if('0.3.' in colorama.__version__):
        print(SUCCESS + 'colorama ' + colorama.__version__)
    else:
        print(WARNING + 'install/upgrade colorama for aesthetic appeal')

    return True

if(not versioning()):
    quit()

colorama.init()