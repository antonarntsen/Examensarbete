import pytest
import requests
from unittest.mock import patch
from app import app, get_weather
import responses
import json

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
    
sample_weather_sunny = {
    "current": {
        "temp_c": 15,
        "condition": {
            "text": "Sunny",
            "icon": "sunny_icon"
        },
        "wind_kph": 10
    }
}

sample_weather_cloudy = {
    "current": {
        "temp_c": 15,
        "condition": {
            "text": "Cloudy",
            "icon": "cloudy_icon"
        },
        "wind_kph": 10
    }
}

@responses.activate
def test_get_weather():
    responses.add(
        responses.GET, 'http://api.weatherapi.com/v1/current.json',
        json=sample_weather_sunny, status=200)

    assert get_weather("fake_api_key", "fake_city") == sample_weather_sunny

# Test cases for different weather conditions
def test_sunny_weather():
    with patch('app.get_weather', return_value=sample_weather_sunny):
        with app.test_client() as client:
            resp = client.post('/', data={'city': 'fake_city'})
            assert b"Use sunscreen, dummy!" in resp.data

def test_cloudy_weather():
    with patch('app.get_weather', return_value=sample_weather_cloudy):
        with app.test_client() as client:
            resp = client.post('/', data={'city': 'fake_city'})
            assert b"The shade feels nice." in resp.data
