from src import manager
from src.models import Apartment
from src.manager import Manager
from src.models import Parameters
from src.models import Bill
from src.models import ApartmentSettlement


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
    
    # 1. Zdefiniowanie mieszkań (żeby Pydantic nie płakał i Manager je widział)
    manager.apartments['apt-1'] = Apartment(
        key='apt-1', 
        name='Apartament 1',
        location='ul. Testowa 1', 
        area_m2=50.0, 
        rooms={}
    )
    manager.apartments['apt-empty'] = Apartment(
        key='apt-empty', 
        name='Puste Mieszkanie',
        location='ul. Pusta 2', 
        area_m2=35.5, 
        rooms={}
    )
    
def test_apartment_settlement_logic():
    parameters = Parameters()
    manager = Manager(parameters)

    manager.apartments['apt-1'] = Apartment(
        key='apt-1',
        name='Apartament 1',
        location='ul. Testowa 1',
        area_m2=50.0,
        rooms={}
    )
    manager.apartments['apt-empty'] = Apartment(
        key='apt-empty',
        name='Puste Mieszkanie',
        location='ul. Pusta 2',
        area_m2=35.5,
        rooms={}
    )

    manager.bills.append(Bill(
        apartment='apt-1',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=200.0,
        type='rent',
        date_due='2024-01-10'
    ))
    manager.bills.append(Bill(
        apartment='apt-1',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=50.0,
        type='electricity',
        date_due='2024-01-15'
    ))
    manager.bills.append(Bill(
        apartment='apt-1',
        settlement_year=2024,
        settlement_month=2,
        amount_pln=100.0,
        type='gas',
        date_due='2024-02-10'
    ))

    settlement_1 = manager.get_apartment_settlement('apt-1', 2024, 1)
    settlement_2 = manager.get_apartment_settlement('apt-1', 2024, 2)
    settlement_empty = manager.get_apartment_settlement('apt-empty', 2024, 1)
    settlement_none = manager.get_apartment_settlement('non-existent', 2024, 1)

    assert settlement_1 is not None
    assert settlement_1.total_bills_pln == 250.0
    assert settlement_1.total_due_pln == -250.0

    assert settlement_2 is not None
    assert settlement_2.total_bills_pln == 100.0
    assert settlement_2.total_due_pln == -100.0

    assert settlement_empty is not None
    assert settlement_empty.total_bills_pln == 0.0
    assert settlement_empty.total_due_pln == 0.0
    assert settlement_empty.month == 1

    assert settlement_none is None