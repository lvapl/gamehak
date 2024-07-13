import requests

base_url = "https://games-test.datsteam.dev/"
headers = {
    'X-Auth-Token': '668f9d09cb8ce668f9d09cb8d2',
    'Content-Type': 'application/json'
}

def send_get_request(url, params=None):
    try:
        response = requests.get(base_url+url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

def send_post_request(url, data=None, json=None):
    try:
        response = requests.post(base_url+url, data=data, json=json, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

def send_put_request(url, data=None, json=None):
    try:
        response = requests.put(base_url+url, data=data, json=json, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
