import requests, json

class shoppy_connection():

    def __init__(self, api_key):
        self.api_key = api_key

    def auth(self, order_id):
        res = requests.get(url='https://shoppy.gg/api/v1/orders/{0}'.format(order_id), headers = {
            'Authorization': '{0}'.format(self.api_key),
            'User-agent': 'Bhop'
            })
        
        if res.status_code == 200:
            # Getting the JSON from Shoppy.
            res_dict = json.loads(res.text)

            # The informations we want.
            config_purchased, paid_at = '', ''

            # Authorizing order.
            auth1, auth2 = False, False

            # Going through the order id.
            for key, value in res_dict.items():
                if key == 'confirmations' and value == 1:
                    auth1 = True
                
                elif key == 'delivered' and value == 1:
                    auth2 = True
                
                elif key == 'paid_at':
                    try:
                        paid_at = str(value[0:10])
                    except:
                        paid_at = ''
                
                elif key == 'product':
                    productStr = str(value)

                    if productStr.__contains__('Aimware'):
                        config_purchased = 'AIMWARE CONFIG'
                    
                    if productStr.__contains__('Neverlose'):
                        config_purchased = 'NEVERLOSE CONFIG'
                    
                    if productStr.__contains__('Gamesense'):
                        config_purchased = 'GAMESENSE CONFIG'
                    
                    if productStr.__contains__('LuckyCharms'):
                        config_purchased = 'LUCKYCHARMS CONFIG'
                    
                    if productStr.__contains__('Onetap'):
                        config_purchased = 'ONETAP CONFIG'

            if auth1 == True and auth2 == True:
                resArray = [config_purchased, order_id, paid_at]

                return resArray
            
            else:

                return ["error"]
        
        else:
            resArray = ['error']

            return resArray