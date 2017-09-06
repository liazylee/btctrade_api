import urllib2
import json
import time
import hashlib
import hmac

import requests

pulick_key='xxx'
secret_key='xxx'

time_delay=2

class BtcTradeApi(object):
    def api_trade_info(self,coin_type):
        try:
            url='https://api.btctrade.com/api/ticker?coin=%s'%(str(coin_type))
            req=urllib2.urlopen(url,timeout=time_delay).read()
            result=json.loads(req)
            return result
        except Exception as e :
            print 'Error_api_trade_info: ',e
            return False

    def api_trade_record(self,coin_type):
        try:
            url='https://api.btctrade.com/api/trades?coin=%s'%(str(coin_type))
            req=urllib2.urlopen(url,timeout=time_delay).read()
            result=json.loads(req)

            return result
        except Exception as e:
            print 'error_trade_recode: ',e
            return False


    def generate_data(self,params):
        md5key=hashlib.md5(secret_key.encode('utf-8')).hexdigest()
        md5key=str(md5key).encode('utf-8')
        dict={}
        dict['key']=pulick_key
        dict['nonce']=str(time.time()).split('.')[0]
        dict['version']='2'
        for key in params:
            dict[key] = params[key]
        string = ''
        for key in dict:
            string += key + '=' + dict[key] + '&'
        string = string[0:-1]
        hmac_encode = hmac.new(md5key, msg=string.encode('utf-8'), digestmod='sha256')
        dict['signature'] = hmac_encode.hexdigest()
        return dict

    def api_get_info(self):
        # get the user information
        url = 'https://api.btctrade.com/api/balance/'
        try:
            response = requests.post(url, data=self.generate_data({}), timeout=timeout_value)
            # print(response.text)
            return json.loads(response.text)
        except Exception as e:
            print('ERROR_API_GET_INFO:  ', e)
            return False


    def api_market_trade(self,coin_type):
        url='https://api.btctrade.com/api/trades?coin=%s' % str(coin_type)

        try:
            req=urllib2.urlopen(url,data=self.generate_data({}),timeout=time_delay).read()
            return json.loads(req)
        except Exception as e:
            print 'ERROR_API_MARKET_TRADES:  ', e
            return False


    def api_get_orders(self,coin_type,order_type,sort_type):
        url='https://api.btctrade.com/api/orders/'

        dic={}
        dic['coin']=str(coin_type)
        dic['type']=str(order_type)
        dic['ob']=str(sort_type)
        try:
            response=requests.post(url,data=self.generate_data(dic)).text
            return json.loads(response)
        except Exception as e:
            print 'ERROR_API_GET_ORFERS :',e
            return  False


    def api_get_fetch_order(self,order_id):
        url='https://api.btctrade.com/api/fetch_order/'

        dic={}
        dic['id']=str(order_id)
        try:
            req=urllib2.urlopen(url,data=self.generate_data(dic)).read()
            return json.loads(req)

        except Exception as e:
            print 'ERROR_API_GET_FETCH_ORDER: ',e
            return False

    def api_cancel_order(self,order_id):
        url='https://api.btctrade.com/api/cancel_order/'
        dic={}
        dic['id']=str(order_id)
        try:
            req=urllib2.urlopen(url,data=self.generate_data(dic)).read()
            return json.loads(req)

        except Exception as e :
            print 'ERROR_CANCEL_ORDER: ',e
            return False

    def api_buy_order(self,coin_type,amount,price):
        url='https://api.btctrade.com/api/buy/'
        dic={}
        dic['coin']=str(coin_type)
        dic['amount']=str(amount)
        dic['price']=str(price)
        try:
            response=requests.post(url,data=self.generate_data(dic))
            return json.loads(response.text)
        except Exception as e:
            print('ERROR_API_BUY_ORDER:  ', e)
            return False

    def api_sell_order(self,coin_type,amount,price):
        url='https://api.btctrade.com/api/sell/'
        dic={}
        dic['coin']=str(coin_type)
        dic['amount']=str(amount)
        dic['price']=str(price)

        try:
            response=requests.post(url,data=self.generate_data(dic)).text
            return json.loads(response)

        except Exception as e:
            print('ERROR_API_SELL_ORDER:  ', e)
            return False


if __name__=='__main__':
    a=BtcTradeApi()
    coin_types=['btc','etc','ltc','eth','doge','ybc']
    for coin_type in coin_types:
        print '%s info is :'%coin_type
        print a.api_trade_info(coin_type)


