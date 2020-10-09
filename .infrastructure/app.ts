import * as cdk from '@aws-cdk/core';
import { Ci } from './stacks/ci';

const app = new cdk.App();

new Ci(app, 'lambda-extensions--parameter-store--infrastructure', {
    env: {
        account: '863125196191', // lambda-extensions account ID
        region: 'us-east-1'
    }
});

