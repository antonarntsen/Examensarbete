import requests

def test_response_status_code():
    response = requests.get('https://api.weatherapi.com/v1/current.json?key=689649eb6e934beaa8591200230805&q=New%20York')
    
    assert response.status_code == 200