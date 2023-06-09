import pytest
import requests

def test_api_responsive():
    response = requests.get('http://api.weatherapi.com/v1/current.json', params={"key": "689649eb6e934beaa8591200230805", "q": "Stockholm", "aqi": "no"})
    assert response.status_code == 200
