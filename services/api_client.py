import requests
from config import Config

def post(endpoint, data):
    url = f"{Config.BASE_API_URL}/{endpoint}"
    headers = {}

    # Add API key header if available
    if Config.FLYNOMIC_API_KEY:
        headers["x-api-key"] = Config.FLYNOMIC_API_KEY
        # If your backend uses Bearer instead:
        # headers["Authorization"] = f"Bearer {Config.FLYNOMIC_API_KEY}"

    print(f"\n➡️  POST {url}")
    print(f"📦  Body: {data}")
    print(f"🔑  Headers: {headers}")

    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"⬅️  Status: {response.status_code}")
        print(f"🔹  Response: {response.text}")

        if not response.ok:
            try:
                return response.json()
            except:
                return {"error": f"HTTP {response.status_code}: {response.text}"}

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return {"error": str(e)}
