import requests
import json

with open('test4') as f:
    payload = json.load(f)

res = requests.post('http://localhost:5000/receipts/process', json=payload)
if res.ok:
    print(res.json())
else:
    print(res)