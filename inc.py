import csv
import os.path
from openpyxl import Workbook
from openpyxl import load_workbook
from datetime import datetime

''' CLIENT CONSTRUCTOR '''

class Client:
    def __init__(self, a_ref, adviser, c_ref, client_f, client_s):
        self.ar = a_ref
        self.a = adviser
        self.cr = c_ref
        self.fn = client_f
        self.sn = client_s
        self.gia_assets = []
        self.isa_assets = []
        self.lisa_assets = []
        self.sipp_assets = []
        self.gia_total = 0
        self.isa_total = 0
        self.lisa_total = 0
        self.sipp_total = 0
        self.gia_cash = 0
        self.isa_cash = 0
        self.lisa_cash = 0
        self.sipp_cash = 0
        self.sipp_fcash = 0
        self.sipp_scash = 0
        self.t = []
        self.fee = []
    
    def add_transaction(self, transactions):
        transaction_list = transactions
        for i, t in enumerate(transactions):
            if(t[2] == self.cr):
                # self.t.appent(Date, Product, Description, Asset, Amount, Quantity, Book, ISIN, SEDOL)
                try:
                    self.t.append([datetime.strptime(t[6], '%d/%m/%Y %H:%M:%S').date(), t[5], t[9], t[10], t[12], t[13], t[20], t[21], t[22]])         # Adds transaction to client transaction list
                except:
                    self.t.append([datetime.strptime(t[6], '%d/%m/%Y %H:%M').date(), t[5], t[9], t[10], t[12], t[13], t[20], t[21], t[22]])         # Adds transaction to client transaction list
    
    def cash(self):
        for fund in self.gia_assets:
            if(fund[2].strip() == 'Cash GBP'):
                self.gia_cash += fund[8]
            else:
                pass
        for fund in self.isa_assets:
            if(fund[2].strip() == 'Cash GBP'):
                self.isa_cash += fund[8]
            else:
                pass
        for fund in self.lisa_assets:
            if(fund[2].strip() == 'Cash GBP'):
                self.lisa_cash += fund[8]
            else:
                pass
        for fund in self.sipp_assets:
            if(fund[2].strip() == 'Cash GBP' or fund[2].strip() == 'Investcentre SIPP Cash Account'):
                self.sipp_cash += fund[8]
                if(fund[2].strip() == 'Cash GBP' or fund[2].strip()):
                    self.sipp_fcash += fund[8]
                if(fund[2].strip() == 'Investcentre SIPP Cash Account'):
                    self.sipp_scash += fund[8]
            else:
                pass
    
    def add_fund(self, product, source, name, sedol, isin, cost, price, units, value, date):
        
        # Settings
        GIA = 'Investcentre Dealing Account'
        ISA = 'Investcentre ISA Stocks and Shares'
        SIPP = 'Investcentre SIPP'
        LISA = 'Investcentre Lifetime ISA'
        
        if(cost == ''):
            cost = value
        
        if(product.lower().strip() == GIA.lower()):
            fund = [product, source, name, sedol, isin, float(cost), float(price), float(units), float(value), date]
            self.gia_assets.append(fund)
            self.gia_total += fund[8]
        elif(product.lower().strip() == LISA.lower()):
            fund = [product, source, name, sedol, isin, float(cost), float(price), float(units), float(value), date]
            self.lisa_assets.append(fund)
            self.lisa_total += fund[8]
        elif(product.lower().strip() == ISA.lower()):
            fund = [product, source, name, sedol, isin, float(cost), float(price), float(units), float(value), date]
            self.isa_assets.append(fund)
            self.isa_total += fund[8]
        elif(product.lower().strip() == SIPP.lower()):
            fund = [product, source, name, sedol, isin, float(cost), float(price), float(units), float(value), date]
            self.sipp_assets.append(fund)
            self.sipp_total += fund[8]
        else:
            print(product.lower())
            print('No Product Found')
            quit()

''' / CLIENT CONSTRUCTOR '''

''' FUNCTIONS '''

def import_csv(file_name):
    fund_list = []
    with open(file_name) as file:
        reader = csv.reader(file)
        fund_list = list(reader)
    return(fund_list)

def add_value(value_line):
    exist = False
    for clients in client_list:
        if(clients.cr == value_line[2]):
            exist = True
            clients.add_fund(value_line[5], value_line[6], value_line[7], value_line[8], value_line[9], value_line[10], value_line[11], value_line[12], value_line[13], value_line[14])
            break
        else:
            exist = False
            pass
    if(exist == False):
        client_list.append(Client(value_line[0], value_line[1], value_line[2], value_line[3], value_line[4]))
        client_list[(len(client_list) - 1)].add_fund(value_line[5], value_line[6], value_line[7], value_line[8], value_line[9], value_line[10], value_line[11], value_line[12], value_line[13], value_line[14])
        
''' / FUNCTIONS '''

''' SETTINGS '''
cash_level = 20000
percent_cap = 0.75
''' / SETTINGS '''

''' MAIN PROGRAM '''

client_list = []

valuation = import_csv('clients.csv')     # Store client csv data to list
print('Clients imported.')

for row in valuation[1:]:
    add_value(row)
print('Client list built.')

for client in client_list:
    client.cash()
print('Cash accounts updated.')

transaction = import_csv('transactions.csv')
print('Transactions imported.')

for client in client_list:
    client.add_transaction(transaction)
print('Transactions added')

for client in client_list:
    client.t.sort(key=lambda r:r[0])
    charges = []
    for t in client.t:
        if(t[2].lower().strip() == 'ongoing adviser charge'):
            charges.append(t)
    if(charges != []):
        client.fee = [[charges[-1][0], charges[-1][4]]]
        try:
            client.fee.append([charges[-2][0], charges[-2][4]])
        except:
            pass
print('Fees updated.')

output_contents = []

for client in client_list:
    gia_percent = 'N/a'
    gia_p = 0
    isa_percent = 'N/a'
    isa_p = 0
    lisa_percent = 'N/a'
    lisa_p = 0
    sipp_percent = 'N/a'
    sipp_p = 0
    if(client.gia_total != 0):
        gia_percent = '{:.1%}'.format((client.gia_cash / client.gia_total))
        gia_p = client.gia_cash / client.gia_total
    else:
        gia_percent = 'N/a'
        gia_p = 0
    if(client.isa_total != 0):
        isa_percent = '{:.1%}'.format((client.isa_cash / client.isa_total))
        isa_p = client.isa_cash / client.isa_total
    else:
        isa_percent = 'N/a'
        isa_p = 0
    if(client.lisa_total != 0):
        lisa_percent = '{:.1%}'.format((client.lisa_cash / client.lisa_total))
        lisa_p = client.lisa_cash / client.lisa_total
    else:
        lisa_percent = 'N/a'
        lisa_p = 0
    if(client.sipp_total != 0):
        sipp_percent = '{:.1%}'.format((client.sipp_cash / client.sipp_total))
        sipp_p = client.sipp_cash / client.sipp_total
    else:
        sipp_percent = 'N/a'
        sipp_p = 0
    if(gia_p >= percent_cap or isa_p >= percent_cap or lisa_p >= percent_cap or sipp_p >= percent_cap):
        if(client.sipp_cash > cash_level or client.isa_cash > cash_level or client.lisa_cash > cash_level or client.gia_cash > cash_level):
            output_contents.append([client.a, client.fn, client.sn, client.gia_cash, gia_p, client.isa_cash, isa_p, client.lisa_cash, lisa_p, client.sipp_cash, sipp_p])
            '''nt('Adviser Name: ' + client.a)
            print('Client Name: ' + client.fn + ' ' + client.sn)
            print('GIA: ' + gia_percent)
            print('ISA: ' + isa_percent)
            print('SIPP: ' + sipp_percent)
            print('\n')'''

output_contents.sort(key=lambda r:r[0])

for thing in output_contents:
    # print(thing)
    print('Adviser: ' + thing[0])
    print('Client: ' + thing[1] + ' ' + thing[2])
    print('GIA Cash: £' + str(thing[3]) + ' (' + str(int(thing[4] * 100)) + ')')
    print('ISA Cash: £' + str(thing[5]) + ' (' + str(int(thing[6] * 100)) + ')')
    print('LISA Cash: £' + str(thing[7]) + ' (' + str(int(thing[8] * 100)) + ')')
    print('SIPP Cash: £' + str(thing[9]) + ' (' + str(int(thing[10] * 100)) + ')')
    print('\n')

'''
        self.ar = a_ref
        self.a = adviser
        self.cr = c_ref
        self.fn = client_f
        self.sn = client_s
        self.gia_assets = []
        self.isa_assets = []
        self.sipp_assets = []
        self.gia_total = 0
        self.isa_total = 0
        self.sipp_total = 0
        self.gia_cash = 0
        self.isa_cash = 0
        self.sipp_cash = 0
        self.sipp_fcash = 0
        self.sipp_scash = 0
        self.t = []
        self.fee = []
'''

''' / MAIN PROGRAM '''
