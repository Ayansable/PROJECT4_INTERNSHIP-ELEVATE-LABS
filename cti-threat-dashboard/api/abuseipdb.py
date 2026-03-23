import requests

# Use your real API key here
API_KEY = "dd2c2bd7ddf255db5afb1a6144fe2f0d445f13fbccccf3f23cce2e9898ec2891d0ee041c742cbb10"

def check_ip(ip):
    url = "https://api.abuseipdb.com/api/v2/check"

    headers = {
        "Accept": "application/json",
        "Key": API_KEY
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        print("HTTP Status:", response.status_code)      # Debug
        print("Response Text:", response.text[:200])     # Debug first 200 chars

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API returned status {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}