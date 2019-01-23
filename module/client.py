from datetime import datetime

class Client:
    def __init__(self, a_ref, adviser, c_ref, first_name, surname):
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
    
    def add_fund(self, valuation):
        existing_account = False
        
        for a in self.accounts:
            if(valuation[5] == a.p):
                # Account found
                existing_account = True
                a.f.append(Fund(valuation[7], valuation[8], valuation[9], valuation[10],
                            valuation[11], valuation[12], valuation[13], valuation[14]))
                print('Account Found: ' + valuation[5])
                break
            else:
                # Account not found, pass for now
                pass
            
        if(existing_account == False):
            # Account not found - adding an account
            self.accounts.append(Account(valuation[14], valuation[5], valuation[2],
                                valuation))
            print('New Account Added: ' + valuation[5])
                
                
                
    
    def add_transaction(self, transaction):
        for a in self.accounts:
            if(transaction[5] == a.p):
                # Account found
                a.t.append(transaction)
            else:
                # Account not found
                pass

class Fund:
    def __init__(self, name, sedol, isin, cost, price, units, value, date):
        self.n = name
        self.s = sedol
        self.i = isin
        self.c = cost
        self.p = price
        self.u = units
        self.v = value
        self.d = date
                
class Account:
    def __init__(self, date, product, c_ref, transaction):
        self.d = date
        self.p = product
        self.cr = c_ref
        
        self.f = []
        self.t = []
        self.new_fund(transaction)
        
        self.v = 0  # value
        self.c = 0  # cash
        
    def update_value(self):
        self.v = 0
        for i in self.f:
            self.v += i.v
    
    def new_fund(self, valuation):
        GIA = 'Investcentre Dealing Account'
        ISA = 'Investcentre ISA Stocks and Shares'
        SIPP = 'Investcentre SIPP'
        LISA = 'Investcentre Lifetime ISA'
        
        self.t.append(valuation)
        self.f.append(Fund(valuation[7], valuation[8], valuation[9], valuation[10],
                            valuation[11], valuation[12], valuation[13], valuation[14]))
        
        
        