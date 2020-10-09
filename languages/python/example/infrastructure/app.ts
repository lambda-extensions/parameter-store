import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as path from 'path';

const app = new cdk.App();

const extensions = {
    account: '863125196191', // lambda-extensions account id
    region: 'us-east-1'
}

const stack = new cdk.Stack(app, 'LambdaExtensionsParameterStoreExample');

const version = stack.node.tryGetContext('EXTENSION_VERSION');

new lambda.Function(stack, 'Function', {
    handler: 'main.handler',
    runtime: lambda.Runtime.PYTHON_3_8,
    code: lambda.Code.fromAsset(path.join(__dirname, '../handler')),
    environment: {
        MY_SECRET: 'ssm.my-secret'
    },
    layers: [
        lambda.LayerVersion.fromLayerVersionArn(stack, 'ParameterStoreExtensionLayer', `arn:aws:lambda:${extensions.region}:${extensions.account}:layer:python-parameter-store-extension:${version}`)
    ]
});
