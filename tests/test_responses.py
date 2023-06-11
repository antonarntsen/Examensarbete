import pytest
import requests
from unittest.mock import Mock
from app import app, get_weather

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_weather(client):
    response = client.get('/')
    assert response.status_code == 200

def test_weather_api_responsive():
    base_url = "http://api.weatherapi.com/v1/current.json"
    api_key = "689649eb6e934beaa8591200230805"
    city = "Stockholm"
    params = {
        "key": api_key,
        "q": city,
        "aqi": "no"
    }
    response = requests.get(base_url, params=params)
    assert response.status_code == 200
    
def create_mock_weather(temp_c, condition_text):
    return {
        "current": {
            "temp_c": temp_c,
            "condition": {
                "text": condition_text,
                "icon": ""
            },
            "wind_kph": 5
        }
    }

def test_sunny_hot_weather(mocker, client):
    mocker.patch('requests.get', return_value=Mock(ok=True))
    requests.get.return_value.json.return_value = create_mock_weather(30, "Sunny")
    response = client.post('/', data={"city": "test"})
    assert b"Use sunscreen, dummy!" in response.data

def test_sunny_cold_weather(mocker, client):
    mocker.patch('requests.get', return_value=Mock(ok=True))
    requests.get.return_value.json.return_value = create_mock_weather(-10, "Sunny")
    response = client.post('/', data={"city": "test"})
    assert b"It's really cold out there." in response.data

def test_cloudy_weather(mocker, client):
    mocker.patch('requests.get', return_value=Mock(ok=True))
    requests.get.return_value.json.return_value = create_mock_weather(20, "Cloudy")
    response = client.post('/', data={"city": "test"})
    assert b"The shade feels nice." in response.data

def test_overcast_weather(mocker, client):
    mocker.patch('requests.get', return_value=Mock(ok=True))
    requests.get.return_value.json.return_value = create_mock_weather(20, "Overcast")
    response = client.post('/', data={"city": "test"})
    assert b"The shade feels nice." in response.data

def test_rainy_weather(mocker, client):
    mocker.patch('requests.get', return_value=Mock(ok=True))
    requests.get.return_value.json.return_value = create_mock_weather(20, "Rain")
    response = client.post('/', data={"city": "test"})
    assert b"Grab an umbrella!" in response.data

def test_cold_weather(mocker, client):
    mocker.patch('requests.get', return_value=Mock(ok=True))
    requests.get.return_value.json.return_value = create_mock_weather(4, "Clear")
    response = client.post('/', data={"city": "test"})
    assert b"Put on a jacket!" in response.data

def test_very_cold_weather(mocker, client):
    mocker.patch('requests.get', return_value=Mock(ok=True))
    requests.get.return_value.json.return_value = create_mock_weather(-10, "Clear")
    response = client.post('/', data={"city": "test"})
    assert b"It's really cold out there." in response.data

def test_misty_weather(mocker, client):
    mocker.patch('requests.get', return_value=Mock(ok=True))
    requests.get.return_value.json.return_value = create_mock_weather(20, "Mist")
    response = client.post('/', data={"city": "test"})
    assert b"It might be hard to see." in response.data

def test_unrecognized_weather(mocker, client):
    mocker.patch('requests.get', return_value=Mock(ok=True))
    requests.get.return_value.json.return_value = create_mock_weather(20, "Unrecognized")
    response = client.post('/', data={"city": "test"})
    assert b"I'm unsure" in response.data
