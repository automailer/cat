from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

cat_data = {
    'breed': 'TestBreed',
    'year': str(datetime.now().year),
    'month': str(datetime.now().month),
    'day': str(datetime.now().day),
    'description': 'TestDescription',
    'color': 'Red',
}

cats = [
    {
        'breed': 'Bulldog',
        'year': str(datetime.now().year),
        'month': str(datetime.now().month),
        'day': str(datetime.now().day),
        'color': 'Brown',
        'description': 'Short-nosed, wrinkled face',
    },
    {
        'breed': 'Siamese',
        'year': str(datetime.now().year),
        'month': str(datetime.now().month),
        'day': str(datetime.now().day),
        'color': 'Blue',
        'description': 'Pointed coat, vocal',
    },
    {
        'breed': 'Persian',
        'year': str(datetime.now().year),
        'month': str(datetime.now().month),
        'day': str(datetime.now().day),
        'color': 'White',
        'description': 'Long, fluffy coat',
    }
]

invalid_cat_data = {
    'breed': 'TestBreed',
    'age': 'invalid_date',
    'description': 'TestDescription',
    'color': 'Red',
}


updated_cat_data = {
    'breed': 'NewBreed',
    'year': str(datetime.now().year),
    'month': str(datetime.now().month),
    'day': str(datetime.now().day),
    'description': 'TestDescription',
    'color': 'Red',
}


def test_create_item():
    response = client.post('/api/v1/cats/', json=cat_data)
    assert response.status_code == 201
    assert response.json()['breed'] == cat_data['breed']


def test_get_item():
    response = client.get('/api/v1/cats/1')  # Assuming ID 1 exists
    assert response.status_code == 200
    assert response.json()['breed'] == cat_data['breed']


def test_get_items():
    for data in cats:
        client.post('/api/v1/cats/', json=data)

    response = client.get('/api/v1/cats/')
    assert response.status_code == 200
    assert response.json()['total'] >= 3


def test_update_item():
    response = client.patch('/api/v1/cats/1', json=updated_cat_data)
    assert response.status_code == 200
    assert response.json()['breed'] == 'NewBreed'


def test_delete_item():
    response = client.delete('/api/v1/cats/1')
    assert response.status_code == 204

    # Try to get deleted item
    get_response = client.get('/api/v1/cats/1')
    assert get_response.status_code == 404


# Test cases for edge conditions

def test_create_item_invalid():

    response = client.post('/api/v1/cats/', json=invalid_cat_data)
    assert response.status_code == 422


def test_get_nonexistent_item():
    response = client.get('/api/v1/cats/99999')
    assert response.status_code == 404


def test_update_nonexistent_item():
    update_data = updated_cat_data
    response = client.patch('/api/v1/cats/99999', json=update_data)
    assert response.status_code == 404


def test_delete_nonexistent_item():
    response = client.delete('/api/v1/cats/99999')
    assert response.status_code == 404


def test_get_all_with_filter():
    response = client.get('/api/v1/cats/?breed=Bulldog')
    assert response.status_code == 200
    assert response.json()['total'] == 1


def test_get_all_without_filter():
    response = client.get('/api/v1/cats/')
    assert response.status_code == 200
    assert response.json()['total'] >= 3


def test_update_item_invalid_date():
    invalid_update_data = invalid_cat_data
    response = client.patch(f"/api/v1/cats/{2}", json=invalid_update_data)
    assert response.status_code == 422
