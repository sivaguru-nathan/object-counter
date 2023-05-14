import requests

class RestApi:
    def __init__(self, url,method):
        self.url = url
        self.method=method
    
    def __call__(self, **kwargs):
        try:
            response = getattr(requests,self.method)(self.url, **kwargs)
            response.raise_for_status()
            print(response)
            return response.json()
        except requests.exceptions.HTTPError as http_error:
            print(f'HTTP error occurred: {http_error}')
        except requests.exceptions.ConnectionError as connection_error:
            print(f'Connection error occurred: {connection_error}')
        except requests.exceptions.Timeout as timeout_error:
            print(f'Timeout error occurred: {timeout_error}')
        except requests.exceptions.RequestException as request_exception:
            print(f'An error occurred: {request_exception}')