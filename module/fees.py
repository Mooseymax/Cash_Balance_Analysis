from datetime import datetime

class Client:
    def __init__(self, a_ref, adviser, c_ref, first_name, surname, val):
        # Logic for having accounts
        self.has_sipp = False
        self.has_isa = False
        self.has_gia = False
        self.has_lisa = False
        
        # Client details
        self.a = adviser
        self.ar = a_ref
        self.fn = first_name
        self.sn = surname
        self.cr = c_ref
        
        # Additional details
        self.accounts = []
        self.add_fund(val)
    
    def details(self):
        print('Client: ' + self.fn + ' ' + self.sn)
        print('Accounts: ' + str(len(self.accounts)))
        for i, acc in enumerate(self.accounts):
            print('  ' + str(i) + '. ' + acc.p)
    
    def add_fund(self, valuation):
        existing_account = False
        
        for a in self.accounts:
            if(valuation[5] == a.p):
                # Account found
                existing_account = True
                a.f.append(Fund(valuation[7], valuation[8], valuation[9], valuation[10],
                            valuation[11], valuation[12], valuation[13], valuation[14]))
                break
            else:
                # Account not found, pass for now
                pass
            #a.update_value()
            
        if(existing_account == False):
            # Account not found - adding an account
            self.accounts.append(Account(valuation[14], valuation[5], valuation[2],
                                valuation))
            #print(self.fn + ' ' + self.sn + ' - New Account Added: ' + valuation[5]) 
               
    def add_transaction(self, transaction):
        existing_account = False
        
        # print(transaction.p)
        
        for a in self.accounts:
            #print(transaction.p + ' || ' + a.p)
            if(transaction.p == a.p):
                # Account found
                a.t.append(transaction)

                existing_account = True
                #print('Transaction added')
                break
            else:
                # Account not found
                pass
        
        if(existing_account == False):
            print(self.fn + ' ' + self.sn)
            print(transaction.p)
            print('Account not found - error')
            #input('')

class Transaction:
    def __init__(self, product, date, desc, name, source, amount, quantity, isin, sedol):
        self.p = product
        # print(str(date).split(' ')[0])
        try:
            self.d = datetime.strptime(str(date).split(' ')[0], '%d/%m/%Y')
        except:
            self.d = date
        self.des = desc
        self.n = name
        self.s = source
        self.a = float(amount)
        if(quantity == ''):
            self.q = 0
        else:
            self.q = float(quantity)
        self.i = isin
        self.sc = sedol
            
class Fund:
    def __init__(self, name, sedol, isin, cost, price, units, value, date):
        self.n = name
        self.s = sedol
        self.i = isin
        self.c = cost
        self.p = price
        self.u = float(units)
        self.v = float(value)
        self.d = date
                
class Account:
    def __init__(self, date, product, c_ref, transaction):
        self.d = date
        self.p = product
        self.cr = c_ref
        
        self.f = []
        self.t = []
        self.i = transaction    # Initial transaction (valuation)
        self.v = 0  # value
        self.sc = 0  # cash
        self.fc = 0 # Funds cash
        
        self.new_fund(Transaction(transaction[5], datetime.today(), 'Initial', 
                        transaction[7], transaction[6], transaction[13],
                        transaction[12], transaction[9], transaction[8]))
        
        #self.update_value()
        
    def low_cash(self):
        income = 0
        for t in self.t:
            if(t.des == 'Ongoing adviser charge'):
                income = t.a
                break
            else:
                pass
        return income
        
    def update_value(self):
        CASH = 'Investcentre SIPP Cash Account'
        CASH_B = 'Cash GBP'
    
        self.v = 0
        self.sc = 0
        self.fc = 0
        
        for i in self.f:
            self.v += i.v
            
            if(i.n.strip() == CASH):
                self.sc += i.v
            
            if(i.n.strip() == CASH_B):
                self.fc += i.v
    
    def new_fund(self, valuation):
        GIA = 'Investcentre Dealing Account'
        ISA = 'Investcentre ISA Stocks and Shares'
        SIPP = 'Investcentre SIPP'
        LISA = 'Investcentre Lifetime ISA'
        
        CASH = 'Investcentre SIPP Cash Account'
        CASH_B = 'Cash GBP'
        
        '''if(valuation.n == CASH or valuation.n == CASH_B):
            self.c += valuation.a
        self.v += valuation.a
        '''
        self.t.append(valuation)
        self.f.append(Fund(self.i[7], self.i[8], self.i[9], self.i[10],
                            self.i[11], self.i[12], self.i[13], self.i[14]))
        
        
        