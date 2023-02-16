
"""
Created on Mon Jan 16 12:33:36 2023

@author: rusha
"""


import requests
import sys
sys.path.insert(0, 'C:/Users/rusha/Quant/')
import Stock_Recommendation_2_OOP

# https://api.telegram.org/bot5952794751:AAHxNKmcSMLMZsi9pkeX-4-HEo965pr-0Vs/getUpdates
# https://api.telegram.org/bot5952794751:AAHxNKmcSMLMZsi9pkeX-4-HEo965pr-0Vs/sendMessage?chat_id=-868916248&text="Test Message"

# chat id :  -868916248

# Stock_Recommendation_2_OOP.nifty.updateDB()

nifty = Stock_Recommendation_2_OOP.Recommender('Nifty')

msg=nifty.recommender()
for i in msg:
    url = f'https://api.telegram.org/bot5952794751:AAHxNKmcSMLMZsi9pkeX-4-HEo965pr-0Vs/sendMessage?chat_id=-868916248&text={i}'
    requests.get(url)


