from src import manager
from src.models import Apartment
from src.manager import Manager
from src.models import Parameters
from src.models import Bill
from src.models import ApartmentSettlement
from src.models import Tenant

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


def test_tenant_settlement_split():
    parameters = Parameters()
    manager = Manager(parameters)
    manager.apartments['apt-1'] = Apartment(
        key='apt-1',
        name='Apartament 1',
        location='Test',
        area_m2=50.0,
        rooms={}
    )
    manager.apartments['apt-2'] = Apartment(
        key='apt-2',
        name='Apartament 2',
        location='Test',
        area_m2=40.0,
        rooms={}
    )
    manager.tenants['t1'] = Tenant(
        key='t1',
        name='A',
        apartment='apt-1',
        room='1',
        rent_pln=1000.0,
        deposit_pln=1000.0,
        date_agreement_from='2024-01-01',
        date_agreement_to='2024-12-31'
    )
    manager.tenants['t2'] = Tenant(
        key='t2',
        name='B',
        apartment='apt-1',
        room='2',
        rent_pln=1000.0,
        deposit_pln=1000.0,
        date_agreement_from='2024-01-01',
        date_agreement_to='2024-12-31'
    )
    manager.tenants['t3'] = Tenant(
        key='t3',
        name='C',
        apartment='apt-2',
        room='1',
        rent_pln=1000.0,
        deposit_pln=1000.0,
        date_agreement_from='2024-01-01',
        date_agreement_to='2024-12-31'
    )
    manager.bills.append(Bill(
        apartment='apt-1',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=300.0,
        type='rent',
        date_due='2024-01-10'
    ))
    manager.bills.append(Bill(
        apartment='apt-2',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=150.0,
        type='rent',
        date_due='2024-01-10'
    ))
    manager.apartments['apt-zero'] = Apartment(
    key='apt-zero',
    name='Zero',
    location='Test',
    area_m2=10.0,
    rooms={}
    )
    settlements = manager.get_tenants_settlement('apt-1', 2024, 1)
    assert settlements is not None
    assert len(settlements) == 2
    values = [s.total_due_pln for s in settlements]
    assert sum(values) == 300.0
    assert values[0] == values[1]  # równy podział
    assert all(v == 150.0 for v in values)
    settlements_single = manager.get_tenants_settlement('apt-2', 2024, 1)
    assert settlements_single is not None
    assert len(settlements_single) == 1
    assert settlements_single[0].total_due_pln == 150.0
    manager.apartments['apt-empty'] = Apartment(
        key='apt-empty',
        name='Empty',
        location='Test',
        area_m2=20.0,
        rooms={}
    )
    settlements_empty = manager.get_tenants_settlement('apt-empty', 2024, 1)
    assert settlements_empty == [] or settlements_empty is None
    assert all(s.total_due_pln >= 0 for s in settlements)
    assert settlements[0].month == 1
    assert settlements[0].year == 2024
    assert all(s.apartment == 'apt-1' for s in settlements)
    settlements_none = manager.get_tenants_settlement('does-not-exist', 2024, 1)
    assert settlements_none is None