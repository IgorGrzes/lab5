from src.models import Apartment
from src.manager import Manager
from src.models import Parameters
from src.models import Bill

def test_load_data():
    parameters = Parameters()
    manager = Manager(parameters)
    assert isinstance(manager.apartments, dict)
    assert isinstance(manager.tenants, dict)
    assert isinstance(manager.transfers, list)
    assert isinstance(manager.bills, list)

    for apartment_key, apartment in manager.apartments.items():
        assert isinstance(apartment, Apartment)
        assert apartment.key == apartment_key

    def test_if_get_apartment_costs():
        parameters = Parameters()
        manager = Manager(parameters)
        assert manager.get_apartment_costs('apart-polanka', 2025, 1) == 910
        assert manager.get_apartment_costs('apart-polanka', 2025, 5) == 0
        assert manager.get_apartment_costs('los', 2025, 5) == None

    def test_apartment_settlement_logic():
        parameters = Parameters()
        manager = Manager(parameters)
        manager.apartments['apt-1'] = Apartment(key='apt-1', name='Apartament 1')
        manager.apartments['apt-empty'] = Apartment(key='apt-empty', name='Puste Mieszkanie')
        
        manager.bills.append(Bill(apartment='apt-1', settlement_year=2024, settlement_month=1, amount_pln=200.0, type='rent'))
        manager.bills.append(Bill(apartment='apt-1', settlement_year=2024, settlement_month=1, amount_pln=50.0, type='electricity'))
        manager.bills.append(Bill(apartment='apt-1', settlement_year=2024, settlement_month=2, amount_pln=100.0, type='gas'))

        settlement_1 = manager.get_apartment_settlement('apt-1', 2024, 1)
        settlement_2 = manager.get_apartment_settlement('apt-1', 2024, 2)
        settlement_empty = manager.get_apartment_settlement('apt-empty', 2024, 1)
        settlement_none = manager.get_apartment_settlement('non-existent', 2024, 1)

        assert settlement_1 is not None
        assert settlement_1.total_bills == 250.0
        assert settlement_1.total_transfers == 0.0
        assert settlement_1.balance == -250.0
        assert settlement_2.total_bills == 100.0
        assert settlement_2.balance == -100.0
        assert settlement_empty is not None
        assert settlement_empty.total_bills == 0.0
        assert settlement_empty.total_transfers == 0.0
        assert settlement_empty.balance == 0.0
        assert settlement_empty.month == 1
        assert settlement_none is None