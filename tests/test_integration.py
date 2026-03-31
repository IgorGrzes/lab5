from src.models import Apartment
from src.manager import Manager
from src.models import Parameters


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