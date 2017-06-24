from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .forms import TradeForm
from .models import Trade
import time
from .bittrex import Bittrex
import json
from decimal import *

with open("bittrextrade/key/secrets.json") as secrets_file:
    secrets = json.load(secrets_file)
    secrets_file.close()
    bittrex = Bittrex(secrets['key'], secrets['secret'])

def index(request):
    currentGMT = time.asctime(time.gmtime())
    form = TradeForm()

    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            if 'buy' in request.POST:
                trade = form.save(commit=False)
                buyResult, myOrderHistory, openOrders = buyCoin(trade.coin)
                # buyCoin(trade.coin)
                return render(request, 'bittrextrade/index.html',
                              {
                                  'currentGMT': currentGMT,
                                  'form': form
                              })
            elif 'sell' in request.POST:
                trade = form.save(commit=False)
                buyResult, myOrderHistory, openOrders = sellCoin(trade.coin)
                return render(request, 'bittrextrade/index.html',
                              {
                                  'currentGMT': currentGMT,
                                  'form': form
                              })
    else:
        form = TradeForm()
        return render(request, 'bittrextrade/index.html',
                      {
                          'currentGMT': currentGMT,
                          'form': form
                      })



def buyCoin(coinName):
    coinName = 'BTC-'+coinName
    askPrice = float('%.8f' % bittrex.get_ticker(coinName)['result']['Ask']) * 1.001
    askPrice = '%.8f' % float(askPrice)
    qty = round(float(0.1 / float(askPrice)), 8)
    buyResult = bittrex.buy_limit(coinName, qty, askPrice)['result']
    myOrderHistory = bittrex.get_order_history(coinName, 1)
    openOrders = bittrex.get_open_orders(coinName)
    return buyResult, myOrderHistory, openOrders

def sellCoin(coinName):
    coinAvail = bittrex.get_balance(coinName)['result']['Available']
    bidPrice = float('%.8f' % bittrex.get_ticker('BTC-'+coinName)['result']['Bid']) * 0.999
    bidPrice = '%.8f' % float(bidPrice)
    buyResult = bittrex.sell_limit('BTC-' + coinName, coinAvail, bidPrice)['result']
    myOrderHistory = bittrex.get_order_history(coinName, 1)
    openOrders = bittrex.get_open_orders(coinName)
    return buyResult, myOrderHistory, openOrders