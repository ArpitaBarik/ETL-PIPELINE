import time
import requests


class APIRequestError(Exception):
    pass


def request_api(
    method,
    url,
    params=None,
    headers=None,
    timeout=10,
    retries=3
):
    for attempt in range(1, retries + 1):
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                timeout=timeout
            )

            print("API URL:", response.url)


            # API CALL HAPPENS HERE
            response.raise_for_status()

            return response.status_code, response.json()

        except requests.exceptions.RequestException as err:
            if attempt == retries:
                raise APIRequestError(err)

            time.sleep(2)
