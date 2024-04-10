import pytest
import requests
from lambda_forge.constants import BASE_URL


@pytest.mark.integration(method="POST", endpoint="/users")
def test_create_user_status_code_is_200():

    response = requests.post(url=f"{BASE_URL}/users", json={"name": "John Doe", "age": 30})

    assert response.status_code == 200
