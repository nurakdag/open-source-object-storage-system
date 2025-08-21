import requests
import os
import pytest
import time

# Gateway'in Docker içindeki adresini kullanıyoruz.
GATEWAY_URL = "http://gateway"

DEFAULT_ADMIN_EMAIL = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@demo.gov.tr")
DEFAULT_ADMIN_PASSWORD = os.getenv("DEFAULT_ADMIN_PASSWORD", "Admin!234")

@pytest.mark.integration
def test_admin_login():
    """
    Gateway üzerinden admin kullanıcısının başarılı bir şekilde giriş yapıp
    JWT token alıp alamadığını test eder. Servislerin ayağa kalkması için
    birkaç deneme yapar.
    """
    login_data = {
        "username": DEFAULT_ADMIN_EMAIL,
        "password": DEFAULT_ADMIN_PASSWORD,
    }

    max_retries = 5
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(f"{GATEWAY_URL}/api/auth/login", data=login_data, timeout=10)
            
            if response.status_code == 200:
                json_response = response.json()
                assert "access_token" in json_response
                assert json_response["token_type"] == "bearer"
                assert "user" in json_response
                assert json_response["user"]["email"] == DEFAULT_ADMIN_EMAIL
                return  # Test başarılı, döngüden çık

            elif response.status_code >= 500:
                print(f"Attempt {attempt + 1}/{max_retries}: Received status {response.status_code}. Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                continue

            else:
                # Diğer 4xx hataları için döngüyü kır
                break

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Connection error: {e}. Retrying in {retry_delay}s...")
            time.sleep(retry_delay)

    # Eğer döngü bittiğinde hala başarılı olamadıysak, son yanıtla fail et
    pytest.fail(f"Could not get a successful response after {max_retries} attempts. Last status code: {response.status_code if 'response' in locals() else 'N/A'}")
