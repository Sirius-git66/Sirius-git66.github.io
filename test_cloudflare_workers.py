import requests
import json

url = "https://solitary-snowflake-grok.sirius-git66.workers.dev/api/grok"
headers = {
    "Content-Type": "application/json"
}
data = {
    "model": "grok-4",
    "messages": [
        {
            "role": "user",
            "content": "Say hi from the future on Nov 9 2025"
        }
    ]
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")