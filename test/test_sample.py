from sample import TestData
import pytest

@pytest.fixture(scope='module')
def db():
    print('*****SETUP*****')
    db = TestData()
    db.connect('data.json')
    yield db
    print('******TEARDOWN******')
    db.close()
def test_billing_data(db):
    billing_data = db.get_data('billing')
    assert billing_data['id'] == 1
    assert billing_data['name'] == 'billing'
    assert billing_data['result'] == 'Ok'
def test_weight_data(db):
    weight_data = db.get_data('weight')
    assert weight_data['id'] == 2
    assert weight_data['name'] == 'weight'
    assert weight_data['result'] == 'Ok'

