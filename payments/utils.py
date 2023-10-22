import requests

url = "https://blockchain.info/tobtc"

def get_BTC_rate(amount, currency):
 params = {"currency": currency, "value": str(amount)}

 response = requests.get(url, params=params)

 if response.status_code == 200:
     bitcoin_value = response.text  
     return bitcoin_value
 else:
     print(f"Failed to fetch data. Status code: {response.status_code}")
     return None