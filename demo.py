import requests 

r = requests.get('http://www.example.com')
print(r.status_code)