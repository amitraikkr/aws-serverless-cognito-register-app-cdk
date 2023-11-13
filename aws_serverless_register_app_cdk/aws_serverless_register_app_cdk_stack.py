from aws_cdk import Stack
from constructs import Construct

from aws_cdk import aws_lambda, aws_apigateway

from aws_cdk.aws_cognito import (
    UserPool, UserPoolClient, VerificationEmailStyle, UserVerificationConfig,
    SignInAliases, AutoVerifiedAttrs, OAuthSettings, OAuthScope,
    UserPoolIdentityProviderGoogle, AttributeMapping, ProviderAttribute
)

class AwsServerlessRegisterAppCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create Cognito User Pool with standard attributes
        user_pool = UserPool(self, "regUserPoolv2",
            self_sign_up_enabled=True,
            user_verification=UserVerificationConfig(
                email_subject="Verify your email for Student app!",
                email_body="Thanks for signing up to our Student app! Your verification code is {####}",
                email_style=VerificationEmailStyle.CODE
            ),
            auto_verify=AutoVerifiedAttrs(email=True),
            sign_in_aliases=SignInAliases(email=True),
            standard_attributes={
                "email": {
                    "required": True,
                    "mutable": True
                }
            }
        )

        # Create User Pool Client for Hosted UI
        user_pool_client = UserPoolClient(self, "regUserPoolClientv2",
            user_pool=user_pool,
            o_auth=OAuthSettings(
                flows={
                    "authorization_code_grant": True
                },
                scopes=[OAuthScope.EMAIL, OAuthScope.OPENID, OAuthScope.PROFILE],
                callback_urls=["https://localhost.com"],
                logout_urls=["https://yourlogouturl.com"]
            )
        )


        # Configure Google as an identity provider
        google_provider = UserPoolIdentityProviderGoogle(self, "GoogleProvider",
            client_id="",
            client_secret="",
            user_pool=user_pool,
            scopes=["profile", "email", "openid"],
            attribute_mapping=AttributeMapping(
                email=ProviderAttribute.GOOGLE_EMAIL,
                given_name=ProviderAttribute.GOOGLE_GIVEN_NAME,
                family_name=ProviderAttribute.GOOGLE_FAMILY_NAME
                # Add other attributes as needed
            )
        )

        # Register Google provider to the User Pool
        user_pool.register_identity_provider(google_provider)

        # Define the Lambda function
        lambda_function = aws_lambda.Function(
            self, "regLambdaFunctionv2",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="index.handler",
            code=aws_lambda.Code.from_asset("lambda")
        )


        # Create an API Gateway
        api = aws_apigateway.RestApi(self, "MyApi",
            rest_api_name="regMyServicev2",
            description="This service serves a lambda output."
        )

        # Create Cognito Authorizer for API Gateway
        authorizer = aws_apigateway.CognitoUserPoolsAuthorizer(
            self, "CognitoAuthorizer",
            cognito_user_pools=[user_pool]
        )

        # Create a Resource and Method on the API Gateway
        resource = api.root.add_resource("myresourcev2")
        resource.add_method(
            "POST",  # or POST, PUT, etc.
            aws_apigateway.LambdaIntegration(lambda_function),
            authorizer=authorizer,
            authorization_type=aws_apigateway.AuthorizationType.COGNITO
        )