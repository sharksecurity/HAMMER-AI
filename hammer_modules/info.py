import requests

def get_info(host):
    url = f"http://ip-api.com/json/{host}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

print(get_info("8.8.8.8"))