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
        
    def get_apartment_costs(self, apartment_key, year = None, month = None):
        
        suma = 0
        
        if apartment_key not in self.apartments:
            return None
                    
        for bill in self.bills:
            if bill.apartment != apartment_key:
                continue
            if year is not None and bill.settlement_year != year:
                continue
            if month is not None and bill.settlement_month != month:
                continue
            suma = suma + bill.amount_pln    
            
        return suma
    
    def AppartmentSettlement(self, apartment_key, year, month):
        if apartment_key not in self.apartments:
            return None
        
        wartosc = self.get_apartment_costs(apartment_key, year, month)
        
        total_transfers = 0.0
        
        return ApartmentSettlement(
            apartment_key=apartment_key,
            year=year,
            month=month,
            total_bills=total_bills,
            total_transfers=total_transfers
        )
    