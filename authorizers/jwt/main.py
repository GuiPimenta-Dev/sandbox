import os
import jwt
import sm_utils

def lambda_handler(event, context):

    # Extract the JWT token from the event
    token = event["headers"].get("authorization")

    # If token is missing, deny access
    if not token:
        return {
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "deny",
                        "Resource": event["methodArn"],
                    }
                ],
            }
        }

    try:
        JWT_SECRET_NAME = os.environ.get("JWT_SECRET_NAME")
        JWT_SECRET = sm_utils.get_secret(JWT_SECRET_NAME)

        # Decode the JWT token
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        effect = "allow"
        email = decoded_token.get("email")
    except:
        effect = "deny"
        email = None

    context = {"email": email}

    # Allow access with the user's email
    return {
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": event["methodArn"],
                }
            ],
        },
        "context": context,
    }
