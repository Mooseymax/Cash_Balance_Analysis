import csv
import os.path
from datetime import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
from module.fees import Client, Account, Fund, Transaction

'''
TRANSACTION COLUMNS
Advised Ref, Adviser Name, Client Reference, Client First Names, Client Surname, Product,
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

valuation = import_csv('v.csv')
print('Clients imported.')

transactions = import_csv('t.csv')
print('Transactions imported.')

for v in valuation[1:]:
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
        client_list.append(Client(v[0], v[1], v[2], v[3], v[4], v))
        #print('New client found: ' + v[3] + ' ' + v[4])

print('Total clients found: ' + str(len(client_list)))
print('')

for t in transactions[1:]:
    existing_client = False
    
    ''' ISSUE HERE'''
    #print(t[3] + str(t[12]))
    transaction = Transaction(t[5], t[6], t[9], t[10], t[11], t[12], t[13], t[21], t[22])
    
    for c in client_list:
        if(t[2] == c.cr):
            existing_client = True
            c.add_transaction(transaction)
            break
        else:
            pass
            
    if(existing_client == False):
        print(t[2] + ' - Transaction not found - possibly removed')
        

print('')
print('Added transactions')
print('')


for c in client_list:
    for a in c.accounts:
        a.update_value()
        a.t.sort(key=lambda x: x.d, reverse=True)
        # loop through transaction
        if(abs(a.low_cash()) > 0 and a.sc / abs(a.low_cash()) < 1 and abs(a.low_cash()) < 3000 and a.p.strip() == 'Investcentre SIPP'):
            print('(' + c.a + ') ' + c.sn + ', ' + c.fn + ' <' + a.p.strip() + '>: Previous Fee = ' + str(abs(a.low_cash())) + ' || SIPP Cash Account = ' + str(a.sc) + ' || F&S Cash: ' + str(a.fc))
        if(abs(a.low_cash()) > 0 and a.fc / abs(a.low_cash()) < 1 and abs(a.low_cash()) < 3000 and not a.p.strip() == 'Investcentre SIPP'):
            print('(' + c.a + ') ' + c.sn + ', ' + c.fn + ' <' + a.p.strip() + '>: Previous Fee = ' + str(abs(a.low_cash())) + ' || F&S Cash: ' + str(a.fc))
            # print(c.sn + ', ' + c.fn + ': ' + str(a.c / abs(a.low_cash())))

        # find first income payment
        # divide cash account by income
        # return how many