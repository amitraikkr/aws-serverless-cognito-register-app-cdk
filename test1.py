import boto3
from botocore.exceptions import ClientError

def authenticate_user(username, password, user_pool_id, client_id):
    client = boto3.client('cognito-idp')

    try:
        auth_response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )

        return {
            'id_token': auth_response['AuthenticationResult']['IdToken'],
            'access_token': auth_response['AuthenticationResult']['AccessToken'],
            'refresh_token': auth_response['AuthenticationResult']['RefreshToken']
        }
    except ClientError as e:
        print(e)
        return None

# Replace these variables with your Cognito details
USER_POOL_ID = ''
CLIENT_ID = ''
USERNAME = ''
PASSWORD = ''

tokens = authenticate_user(USERNAME, PASSWORD, USER_POOL_ID, CLIENT_ID)

if tokens:
    print("ID Token:", tokens['id_token'])
    print("Access Token:", tokens['access_token'])
    print("Refresh Token:", tokens['refresh_token'])
else:
    print("Authentication failed")
