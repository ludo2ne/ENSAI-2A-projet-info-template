import requests
import streamlit as st

DEFAULT_TIMEOUT = st.secrets.get("API_TIMEOUT", 5)


class APIClient:
    def __init__(self, base_url: str, timeout: int = DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, method: str, path: str, **kwargs):
        url = f"{self.base_url}{path}"

        try:
            response = self.session.request(
                method=method, url=url, timeout=kwargs.pop("timeout", self.timeout), **kwargs
            )
            response.raise_for_status()

            if response.headers.get("Content-Type", "").startswith("application/json"):
                return {
                    "status_code": response.status_code,
                    "data": response.json()
                    if "application/json" in response.headers.get("Content-Type", "")
                    else response.text,
                }

            return response.text

        except requests.exceptions.Timeout:
            st.error("⏱️ Le serveur met trop de temps à répondre.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Impossible de se connecter au serveur.")
        except requests.exceptions.HTTPError:
            st.error(f"❌ Erreur HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Erreur inconnue : {e}")

        return None

    def get(self, path: str, params=None, **kwargs):
        return self._request("GET", path, params=params, **kwargs)

    def post(self, path: str, json=None, data=None, **kwargs):
        return self._request("POST", path, json=json, data=data, **kwargs)

    def put(self, path: str, json=None, data=None, **kwargs):
        return self._request("PUT", path, json=json, data=data, **kwargs)

    def delete(self, path: str, **kwargs):
        return self._request("DELETE", path, **kwargs)


API_URL = st.secrets.get("API_URL", "http://localhost:5000")
api_client = APIClient(API_URL)
