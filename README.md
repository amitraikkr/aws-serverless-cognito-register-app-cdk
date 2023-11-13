<h1>A Serverless Application : AWS Cognito with Google Sign-In</h1>

<h2>Overview</h2>

This demonstrates the integration of AWS Cognito with Google as an identity provider. It includes a setup for an API Gateway that authenticates requests using the configured AWS Cognito User Pool and routes authenticated requests to an AWS Lambda function.

<h2>Features</h2>
<ul>
<li>AWS Cognito User Pool with Google Sign-In</li>
<li>Lambda function integration</li>
<li>Secured API endpoints using Cognito User Pools</li>
<li>Infrastructure as Code using AWS CDK</li>
<ul>

<h2>Prerequisites</h2>
<ul>
<li>AWS Account</li>
<li>AWS CLI configured with appropriate permissions</li>
<li>Node.js and npm (for AWS CDK)</li>
<li>Python 3.x (for Lambda functions)</li>
<li>Google Developer Account (for OAuth 2.0 credentials)</li>
</ul>

<h2>Setup and Deployment</h2>

<h3>Step 1: Configure Google OAuth 2.0 Credentials</h3>
<ul>
<li>Go to the Google Developer Console.</li>
<li>Create a project and configure the OAuth consent screen.</li>
<li>Create credentials (OAuth client ID) and note down the Client ID and Client Secret.</li>
</ul>

<h3>Step 2: Deploy AWS Infrastructure</h3>
<ul>
<li>Install AWS CDK: npm install -g aws-cdk</li>
<li>Navigate to the CDK directory and run npm install to install dependencies.</li>
<li>Deploy the stack: cdk deploy</li>
</ul>

<h3>Step 3: Configure AWS Cognito</h3>
<ul>
<li>Open the AWS Cognito console and select your User Pool.</li>
<li>Under "Identity providers", configure Google with the credentials obtained in Step 1.</li>
<li>In "App client settings", enable Google as an identity provider and configure callback and sign-out URLs.</li>
</ul>

<h3>Step 4: Test the Setup</h3>
<ul>
<li>Navigate to the Cognito Hosted UI (URL found in the App client settings).</li>
<li>Test the sign-in flow using Google.</li>
<li>Use Postman or a similar tool to test secured API endpoints.</li>
</ul>
<h2>Lambda Function</h2>

The Lambda function code is located in the lambda directory. It's a simple Python function that returns a "Hello World" message.

<h2>API Gateway</h2>

The API Gateway is configured to authenticate requests using the Cognito User Pool. It routes authenticated requests to the Lambda function.

