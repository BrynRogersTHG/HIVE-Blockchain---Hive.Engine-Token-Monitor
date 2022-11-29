
# Token Monitor for hive.engine v.1.0
# Bryn Rogers - 2022, HIVE (@slobberchops)


from hiveengine.api import Api

import time
import winsound
import os

os.system("")  # enables ansi escape characters in terminal
api = Api()
token = "GLX"
highest, lowest, lastprice, increase, delay = 0, 100, 1, 0, 5

# --------------------------------------------------------------------
# StdOut console colour definitions


class BCOLORS:

    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# --------------------------------------------------------------------
# --------------------------------------------------------------------
# Play Sound if price drops or rises suddenly


def playalert(frequency):

    duration = 1000  # milliseconds
    freq = frequency  # Hz
    winsound.Beep(freq, duration)

    return

# --------------------------------------------------------------------
# --------------------------------------------------------------------
# Returns the Highest Offer from the Buybook for Token


def gethighoffer(strtoken):

    book = (api.find("market", "buyBook", query={"symbol": strtoken}))
    straccount = ""
    fprice = 0
    fquantity = 0
    for high in book:
        if float(high['price']) > fprice:
            straccount = high['account']
            fprice = float(high['price'])
            fquantity = float(high['quantity'])

    return straccount, fprice, fquantity

# --------------------------------------------------------------------
# --------------------------------------------------------------------
# Main Loop; endless loop!


dontdisplayinitalprice = True
print(BCOLORS.OKGREEN + f"Starting up Hive.Engine Token Monitor ({token})..." + BCOLORS.ENDC)


while True:
    account, price, quantity = gethighoffer(token)

    if price < lowest:
        lowest = price

    if price > highest:
        highest = price

    if not dontdisplayinitalprice:

        # No Price Change, display in regular colours
        if lastprice == price:
            print(f'({token}) Buyer - {account}  Buying At - {price} Quantity - {quantity} - Low Price: {lowest}'
                  f'- High Price: {highest}')

        # Price has increased, GREEN!
        elif lastprice < price:
            increase = round((price - lastprice) / lastprice * 100, 4)
            print(BCOLORS.OKGREEN + f'({token}) Buyer - {account}  Buying At - {price} Quantity - {quantity}'
                  f'- Low Price: {lowest} - High Price: {highest}, Up by {increase}%!' + BCOLORS.ENDC)

            # High beep if token raises by 1% or more
            if increase > 1:
                playalert(440)

        # Price has decreased, RED!
        else:
            decrease = round((lastprice - price) / lastprice * 100, 4)
            print(BCOLORS.FAIL + f'({token}) Buyer - {account}  Buying At - {price} Quantity - {quantity}'
                  f'- Low Price: {lowest} - High Price: {highest}, DOWN by {decrease}% :(' + BCOLORS.ENDC)

            # Low beep if token drops by 1% or more
            if decrease > 1:
                playalert(220)

    dontdisplayinitalprice = False
    lastprice = price
    time.sleep(delay)

#comment