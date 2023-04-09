import requests
import json
import random
import string

# Define the API endpoint
url = "http://localhost:5000"

# Generate random data for the request body
def random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def random_float():
    return round(random.uniform(0, 1), 3)

def random_tags():
    return random.choices(['tag1', 'tag2', 'tag3', 'tag4'], k=2)

def random_pred():
    return {
        "image_frame": random_string(50),
        "prob": random_float(),
        "tags": random_tags()
    }

def random_request():
    return {
        "device_id": random_string(10),
        "client_id": random_string(10),
        "created_at": "2023-02-07 14:56:49.386042",
        "data": {
            "license_id": random_string(10),
            "preds": [random_pred() for _ in range(random.randint(1, 5))]
        }
    }

# Send 1000 random requests to the API
for i in range(1000):
    request_data = json.dumps(random_request())
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=request_data, headers=headers)
    print(response.text)
