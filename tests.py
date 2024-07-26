
import requests
import json

test_dict = {
    "test1": 28,
    "test2": 109,
    "test3": 31,
    "test4": 15
}

def test():
    for file, points in test_dict.items():
        with open(file) as f:
            payload = json.load(f)

        res = requests.post('http://localhost:5000/receipts/process', json=payload)
        id = res.json()["id"]
        res = requests.get(f"http://localhost:5000/receipts/{id}/points")
        assert res.json()["points"] == test_dict[file]

test()