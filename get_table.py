import json
from api.cline import *

api = Cline()

account = input("Account name :\t\n")
table = input("Table name :\t\n")

tableJs = api.get_table(account, account, table, limit=2000)

with open(f'tables/{account}.{table}.json', 'w') as fp:
    json.dump(tableJs, fp,indent=4)