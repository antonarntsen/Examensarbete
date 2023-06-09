import pytest
import requests
from unittest.mock import patch
from app import app, get_weather

def test_api_responsive():
    response = requests.get('http://api.weatherapi.com/v1/current.json', params={"key": "689649eb6e934beaa8591200230805", "q": "Stockholm", "aqi": "no"})
    assert response.status_code == 200

def test_get_weather(mocker):
    mocker.patch('requests.get')
    import requests
    requests.get.return_value.json.return_value = {"current": {"temp_c": 20, "condition": {"text": "Sunny", "icon": "icon_url"}, "wind_kph": 10}}

    result = get_weather('api_key', 'city')
    assert result == {"current": {"temp_c": 20, "condition": {"text": "Sunny", "icon": "icon_url"}, "wind_kph": 10}}

def test_get_weather_no_data(mocker):
    mocker.patch('requests.get')
    import requests
    requests.get.return_value.json.return_value = {"error": "No data"}

    result = get_weather('api_key', 'city')
    assert result == None

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_get(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_index_post_sunny_weather(mocker, client):
    mocker.patch('your_flask_app_file.get_weather')
    get_weather.return_value = {"current": {"temp_c": 20, "condition": {"text": "Sunny", "icon": "icon_url"}, "wind_kph": 10}}

    rv = client.post('/', data={'city': 'San Francisco'})
    assert b"Use sunscreen, dummy!" in rv.data

def test_index_post_no_weather_data(mocker, client):
    mocker.patch('your_flask_app_file.get_weather')
    get_weather.return_value = None

    rv = client.post('/', data={'city': 'Unknown City'})
    assert b"Cannot find weather data for Unknown City. Please try again." in rv.data
