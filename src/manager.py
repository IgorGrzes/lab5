from src.models import Apartment, Bill, Parameters, Tenant, Transfer


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)
        
    def get_apartment_costs(self, apartment_key, year, month):
        
        suma = 0
        
        if apartment_key not in self.apartments:
            return None
                    
        for bill in self.bills:
            if bill.apartment != apartment_key:
                continue
            if bill.settlement_month != month:
                continue
            if bill.settlement_year != year:
                continue
            suma = suma + bill.amount_pln    
            
        return suma
        