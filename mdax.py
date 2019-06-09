import requests
import pandas as pd
import json
import yfinance as yf
from pandas_datareader import data
import os
import datetime


class mdax:

    def __init__(self):
        filename = './mdax.pkl'
        try:
            if not self.LoadData(filename):
                self.mdax = pd.DataFrame(pd.read_csv("mdax.csv", sep=";"))
                self.mdax.columns = ['ISIN', 'NAME']
                self.mdax['SYMBOL'] = ''
                # print(self.mdax)
                for index, row in self.mdax.iterrows():
                    self.mdax.loc[index, ['SYMBOL']] = self.isin2symbol(row[0])
                self.mdax.to_csv('./mdax_withSymbols.csv')
                self.mdaxData = self.Download()
                self.mdaxData.to_pickle(filename)

                # print(self.mdax)
        except Exception as ex:
            print(ex)

    def isin2symbol(self, isin):
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={isin}&quotesCount=6&newsCount=0&quotesQueryId=tss_match_phrase_query&multiQuoteQueryId=multi_quote_single_token_query&newsQueryId=news_ss_symbols&enableCb=false&enableNavLinks=false"
        try:
            response = requests.get(url, timeout=2)
            j = json.loads(response.text)
            return (self.getSymbol(j))
        except Exception as ex:
            print(ex)

    def getSymbol(self, j):
        q = j['count']

        for x in j['quotes']:
            if x['exchange'] == 'GER':
                return (x['symbol'])
        return (j['quotes'][0]['symbol'])

    def Download(self):
        endDate = datetime.date.today().strftime("%Y-%m-%d")
        data = yf.download(self.mdax['SYMBOL'].tolist(
        ), start="2009-01-01", end=endDate)
        return (data)

    def LoadData(self, filename):
        if os.path.isfile(filename):
            self.mdaxData = pd.read_pickle(filename)
            return (True)
        else:
            return (False)
