import * as cdk from '@aws-cdk/core';
import { readdirSync } from 'fs';
import { join } from 'path';
import { Ci } from './stacks/ci';
import { Layers } from './stacks/layers';

const app = new cdk.App();
const appName = `lambda-extensions--parameter-store`;
const account = '863125196191'; // lambda-extensions account ID

new Ci(app, `${appName}--infrastructure`, {
    env: {
        account, 
        region: 'us-east-1'
    }
});

const regions = ['us-east-1']

regions.map(region => {
    const paths = readdirSync(join(__dirname, '../languages'));
    new Layers(app, `${appName}--layers--${region}`, {
        layerPaths: paths.map(path => join(__dirname, '../languages', path)),
        env: {
            account,
            region
        }
    })
})
