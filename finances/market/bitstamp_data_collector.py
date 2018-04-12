# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 19:30:18 2017

@author: Pedro
"""

import bitstamp.client as bts
import time
import pandas as pd
import datetime
import numpy as np


import os

cfd = os.path.dirname(os.path.realpath(__file__))

exchanges_data_path = os.path.join(cfd, 'data_base', 'exchanges')

def bitstamp_current_prices():

    bitstamp_public = bts.Public()

    current_prices = {
    'btc-eur': 0, 'eth-eur': 0, 'ltc-eur': 0, 'xrp-eur':0, 'bch-eur':0,
    'eth-btc': 0, 'ltc-btc': 0, 'xrp-btc':0, 'bch-btc':0,
    }

    for coin_pair in list(current_prices.keys()):
        base=coin_pair.split('-')[0]
        quote=coin_pair.split('-')[1]
        try:
            current_prices[coin_pair] = float(bitstamp_public.ticker(base=base, quote=quote)['last'])
            print('updated {}'.format(coin_pair))
        except:
            current_prices[coin_pair] = np.nan
            print('Coin pair {} raised error at time {}'.format(coin_pair, datetime.datetime.now()))

    return current_prices


def create_bitstamp_data_chunk(n_values, step_in_mins):
    prices_data = []
    times_list = []

    for k in range(n_values):
        times_list.append(datetime.datetime.now())
        prices_data.append(bitstamp_current_prices())
        if k < n_values-1:
            time.sleep(step_in_mins*60)

    data_chunk = pd.DataFrame(
        data=prices_data,
        index=times_list)

    return data_chunk

def update_bitstamp_data(new_data_chunk):

    bitstamp_csv_path = os.path.join(exchanges_data_path, 'bitstamp_high_frequency_data.csv')
    # if not os.path.exists(bitstamp_csv_path):

    prices_df = pd.read_csv(
        bitstamp_csv_path,
        index_col=0,
        parse_dates=True,
        infer_datetime_format=True
    )

    prices_df.append(new_data_chunk)
    prices_df.to_csv(bitstamp_csv_path)

    print('Data saved at {}'.format(datetime.datetime.now()))

if __name__=='__main__':
    bitstamp_csv_path = os.path.join(exchanges_data_path, 'bitstamp_high_frequency_data.csv')
    a = create_bitstamp_data_chunk(2, 0.5)
    a.to_csv(bitstamp_csv_path)