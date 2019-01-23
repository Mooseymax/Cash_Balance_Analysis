import csv
import os.path
from datetime import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
from module.client import Client, Account

'''
TRANSACTION COLUMNS
Adviser Name, Client Reference, Client First Names, Client Surname, Product,
Transaction Datetime, Effective Date, Settlement Date, Transaction Description, Asset Name,
Transaction Source, Transaction Amount, Quantity, Dealing Charge, Stamp Duty,
Reference, Venue, Currency Amount, Currency, Book Cost,
ISIN, SEDOL

22 Columns
'''

'''
VALUATION COLUMNS
Adviser Reference, Adviser Name, Client Reference, Client First Names, Client Surname,
Product, Asset Source, Asset Name, SEDOL Code, ISIN Code,
Cost, Price, Units, Value, Valuation Date,
Pending IP Movement

16 Columns
'''

def import_csv(file_name):
    data = []
    with open(file_name) as file:
        reader = csv.reader(file)
        data = list(reader)
        return(data)

client_list = []

valuation = import_csv('test-v.csv')
print('Clients imported.')

transactions = import_csv('test-t.csv')
print('Transactions imported.')

for v in valuation:
    existing_client = False
    
    # Loop through all existing clients to check for match
    for c in client_list:
        if(v[2] == c.cr):
            # Client found in list of clients
            existing_client = True
            c.add_fund(v)
            break
        else:
            # Client not found yet - will remain False if not on list
            pass
    
    if(existing_client == False):
        # Create new client
        client_list.append(Client(v[0], v[1], v[2], v[3], v[4]))
        #print('New client found: ' + v[3] + ' ' + v[4])

print(len(client_list))
print(client_list[1].fn)
print(len(client_list[1].accounts))
    
for fund in client_list[1].accounts[0].f:
    print(fund.n)
