# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 19:30:18 2017
 
@author: Pedro
"""
import sys
import os
sys.path.append('C:\\projects\\finances.git\\finances')

import bitstamp.client as bts
from pprint import pprint
import time
import pandas as pd

public_client = bts.Public()

import time

def strategy_decision(
    current_price,
    stoploss_value,
    cash,
    coin_amount,
    state,
    reinvest_gap=0.2,
    pct_gap=0.025,
    fee=0.0025):

    if cash==0 and coin_amount>0:
        if current_price < stoploss_value*(1-pct_gap) and state == 0:
            cash = coin_amount*current_price*(1-fee)
            coin_amount = 0
            stoploss_value=current_price
            print('sold for {}'.format(current_price))

        elif current_price < stoploss_value*(1+pct_gap) and state == 1:
            cash = coin_amount*current_price*(1-fee)
            coin_amount = 0
            print('sold for {}'.format(current_price))

        elif current_price>stoploss_value*(1+reinvest_gap) and state==1:
            stoploss_value=stoploss_value*(1+reinvest_gap)

    elif coin_amount==0 and cash>0:
        if current_price > stoploss_value*(1+pct_gap) and state==0:
            coin_amount = cash/(current_price)*(1-fee)
            cash = 0
            stoploss_value=current_price
            print('bought for {}'.format(current_price))

        elif current_price > stoploss_value*(1-pct_gap) and state == -1:
            coin_amount = cash/(current_price)*(1-fee)
            cash = 0
            print('bought for {}'.format(current_price))

        elif current_price<stoploss_value*(1-reinvest_gap) and state==-1:
            coin_amount = cash/(stoploss_value*(1-reinvest_gap))*(1-fee)
            cash = 0
            stoploss_value=stoploss_value*(1-reinvest_gap)
            print('bought for {}'.format(current_price))
    
    return cash, coin_amount

def stoploss_strategy(trading_client, reinvest_gap=0.2, pct_gap=0.025, fee=0.0025, invested_value=100):
    ticker = trading_client.ticker(base='btc', quote='eur')
    stoploss_value = float(ticker['last'])
    coin_amount = invested_value/float(ticker['last'])*(1-fee)
    cash = 0
    state = 0

    trade_value = [invested_value]
    stoploss=[stoploss_value]

    while True:
        try:
            current_price = float(trading_client.ticker(base='btc', quote='eur')['last'])
            print('CURRENT PRICE: {}'.format(current_price))
        except:
            pass

        cash, coin_amount = strategy_decision(
            current_price=current_price,
            cash=cash,
            stoploss_value=stoploss_value,
            coin_amount=coin_amount,
            state=state,
            reinvest_gap=reinvest_gap,
            pct_gap=pct_gap,
            fee=fee)

        if current_price >= stoploss_value*(1+pct_gap):
            state=1

        elif current_price <= stoploss_value*(1-pct_gap):
            state=-1

        else:
            state=0

        value = coin_amount*current_price+cash
        trade_value.append(value)
        stoploss.append(stoploss_value)
        print(value)
        time.sleep(10)

 
trading_client = bts.Trading(
       username='769101',
       key='2lAZXUmlwLQfhc80QPcHgFxbhvMSlmY6',
       secret='Z4yacXGzh7LrBcIUqdDjkOfvH5lEcyQZ'
       )

print(trading_client.account_balance())
# stoploss_strategy(trading_client)