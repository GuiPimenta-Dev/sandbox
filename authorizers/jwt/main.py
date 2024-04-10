import jwt


def generate_policy(effect, resource):
    policy = {
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {"Action": "execute-api:Invoke", "Effect": effect, "Resource": resource}
            ],
        }
    }
    return policy


def lambda_handler(event, context):
    # Extract the JWT token from the event
    token = event.get("authorizationToken")

    # If token is missing, deny access
    if not token:
        return {
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Deny",
                        "Resource": event["methodArn"],
                    }
                ],
            }
        }

    try:
        # Decode the JWT token
        decoded_token = jwt.decode(token, "abc", algorithms=["HS256"])
        effect = "Allow"
        email = decoded_token.get("email")
    except:
        effect = "Deny"
        email = None

    context["email"] = email

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
        }
    }
