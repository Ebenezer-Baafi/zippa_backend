import requests

BASE = 'http://127.0.0.1:8000/api/v1'

r = requests.post(f'{BASE}/auth/login/', json={
    'email': 'rider1@zippa.com',
    'password': 'password123',
})
print('Login status:', r.status_code)

if r.status_code != 200:
    print('Login failed:', r.json())
    exit()

token = r.json()['access']
h = {'Authorization': f'Bearer {token}'}

r2 = requests.get(f'{BASE}/jobs/list/?scope=my', headers=h)
print('List status:', r2.status_code)
print('List data:', r2.json())