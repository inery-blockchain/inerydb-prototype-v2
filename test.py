import requests, json
import os
from api.cline import Cline
#r = requests.request('get', url='https://23.88.68.179/v1/chain/get_info', verify=False)
#print(r.content)
#ha = input('input\n')
#os.mkdir(f'generator/contracts/{ha}')
'''   
      "name": "newaccount",
      "base": "",
      "fields": [{
          "name": "creator",
          "type": "name"
        },{
          "name": "name",
          "type": "name"
        },{
          "name": "owner",
          "type": "authority"
        },{
          "name": "active",
          "type": "authority"
        }
'''
def operation(mod) : 
    api = Cline()
    account = input("Enter Account Name : ")    
    
    #is_account = api.get_account(account)


    payload = {
        "account": "inery",
        "name": "newaccount",
        "authorization": [{
            "actor": "createacc",
            "permission": "owner",
        }],
    }
    arguments = {
        
    }

    # Converting payload to binary
    data = api.abi_json_to_bin(account, "newaccount", arguments)
    payload['data'] = data['binargs']

    # final transaction formed
    trx = {"actions": [payload]}
    trx['expiration'] = str((dt.datetime.utcnow() + dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))

    key = keys.INRKey(privatekey)

    resp = api.push_transaction(trx, key, broadcast=True)