import requests


def call_gemini_api(api_url, api_key, payload):
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(f"{api_url}?key={api_key}", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"Gemini API isteği başarısız: {e}")
    except KeyError:
        raise Exception("Yanıt formatı beklenenden farklı")