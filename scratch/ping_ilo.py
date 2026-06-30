import httpx

url = "http://127.0.0.1:8010/redfish/v1/"
try:
    resp = httpx.get(url, timeout=3.0)
    print(f"STATUS: iLO Mock Server is running at {url}. HTTP Response Status: {resp.status_code}")
except Exception as e:
    print(f"STATUS: iLO Mock Server at {url} failed to respond. Error: {e}")
