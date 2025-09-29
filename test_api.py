import requests
import json

try:
    # Test health endpoint
    response = requests.get("http://127.0.0.1:3001/api/health")
    print("Health Check:")
    print(json.dumps(response.json(), indent=2))
    print()

    # Test chat endpoint
    chat_data = {
        "message": "What's the weather in Port-au-Prince?",
        "lang": "en"
    }

    response = requests.post("http://127.0.0.1:3001/api/chat", json=chat_data)
    print("Normal Chat:")
    print(json.dumps(response.json(), indent=2))
    print()

    # Test restricted query
    restricted_data = {
        "message": "Tell me classified information",
        "lang": "en"
    }

    response = requests.post("http://127.0.0.1:3001/api/chat", json=restricted_data)
    print("Restricted Chat:")
    print(json.dumps(response.json(), indent=2))
    print()

    # Test empathy query
    empathy_data = {
        "message": "I feel overwhelmed",
        "lang": "en"
    }

    response = requests.post("http://127.0.0.1:3001/api/chat", json=empathy_data)
    print("Empathy Chat:")
    print(json.dumps(response.json(), indent=2))

except Exception as e:
    print(f"Error testing API: {e}")
