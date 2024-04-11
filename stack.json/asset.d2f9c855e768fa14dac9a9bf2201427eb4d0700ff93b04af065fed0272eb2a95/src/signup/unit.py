import json

from .main import lambda_handler


# Test the create user function leveraging the users_table fixture from the conftest.py file automatically imported by pytest.
def test_lambda_handler(users_table):
    # Simulate an event with a request body, mimicking a POST request payload containing a user's name and age.
    event = {"body": json.dumps({"name": "John Doe", "age": 30})}

    # Invoke the `lambda_handler` function with the simulated event and `None` for the context.
    response = lambda_handler(event, None)

    # Parse the JSON response body to work with the data as a Python dictionary.
    response = json.loads(response["body"])

    # Retrieve the user item from the mocked DynamoDB table using the ID returned in the response.
    # This action simulates the retrieval operation that would occur in a live DynamoDB instance.
    user = users_table.get_item(Key={"PK": response["user_id"]})["Item"]

    # Assert that the name and age in the DynamoDB item match the input values.
    # These assertions confirm that the `lambda_handler` function correctly processes the input
    # and stores the expected data in the DynamoDB table.
    assert user["name"] == "John Doe"
    assert user["age"] == 30
