import datetime as dt
import pytz, argparse

from api.cline import Cline
import api.keys as keys
from api.utils import *


def operation(mod) : 
    api = Cline()

    account = input("Enter Account Name : ")
    #is_account = api.get_account(account)
    privatekey = input("Enter Private key of your account: \n")

    table = input("Enter table : \n")

    action = mod + table
    arguments = api.get_arguments(account, action)

    payload = {
        "account": account,
        "name": action,
        "authorization": [{
            "actor": account,
            "permission": "owner",
        }],
    }

    # Converting payload to binary
    data = api.abi_json_to_bin(account, action, arguments)
    payload['data'] = data['binargs']

    # final transaction formed
    trx = {"actions": [payload]}
    trx['expiration'] = str((dt.datetime.utcnow() + dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))

    key = keys.INRKey(privatekey)
    

    resp = api.push_transaction(trx, key, broadcast=True)


parser = argparse.ArgumentParser()

parser.add_argument("--create", help="Create object in table", action='store_true')
parser.add_argument("--update", help="Update existing object with given id", action='store_true')
parser.add_argument("--delete", help="Delete existing object with given id", action='store_true')

args = parser.parse_args()

if args.create :
    mod = 'cr'
    operation(mod)

if args.update : 
    mod = 'up'
    operation(mod)

if args.delete : 
    mod = 'dl'
    operation(mod)