import logging

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

            data = None
            try:
                data = response.json()
            except Exception:
                data = response.text

            return {"status_code": response.status_code, "data": data}

        except requests.exceptions.Timeout:
            return {"status_code": 0, "data": "Timeout"}
        except requests.exceptions.ConnectionError:
            return {"status_code": 0, "data": "Connection error"}
        except requests.exceptions.RequestException as e:
            return {"status_code": 0, "data": str(e)}
        finally:
            logging.info(f"{response.status_code or 0} {method} {url}")
            logging.info(f"\t{data}")

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
