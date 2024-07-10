from datetime import datetime

import pytest


@pytest.fixture
def base_data():
    return {"date": "31.01.2021", "periods": 3, "amount": 10000, "rate": 6}


@pytest.mark.parametrize("data",
                         ({"date": "31.01.2021", "periods": 3, "amount": 10000, "rate": 6},
                          {"date": "31.03.2021", "periods": 5, "amount": 11000, "rate": 3},
                          {"date": "30.09.2024", "periods": 59, "amount": 11123, "rate": 2}))
def test_success(client, data):
    response = client.post("/calculate", json=data)
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert len(response_data) == data['periods']
    for key, value in response_data.items():
        datetime.strptime(key, '%d.%m.%Y').date()
        assert isinstance(value, int), (key, value)


@pytest.mark.parametrize("method", ['get', 'put', 'delete', 'patch'])
def test_unavailable_methods(client, method, base_data):
    response = client.request(method, f"/calculate", json=base_data)
    assert response.status_code == 405, response.text


@pytest.mark.parametrize("field, value",
                         [('date', '01.31.2021'), ('date', '2021-01-31'), ('date', '123'), ('date', 'today'),
                          ('date', '30.02.2021'), ('date', 1),
                          ('periods', 0), ('periods', -1), ('periods', 61), ('periods', 'all'),
                          ('amount', 0), ('amount', -1), ('amount', 9_999), ('amount', 3_000_001),
                          ('amount', 'undefined'),
                          ('rate', 0), ('rate', -1), ('rate', 9), ('rate', 'undefined')])
def test_invalid_date(client, field, value, base_data):
    data = base_data | {field: value}
    response = client.post("/calculate", json=data)
    assert response.status_code == 400, response.text
    error = response.json().get('error')
    assert isinstance(error, str), error
    assert field in error
