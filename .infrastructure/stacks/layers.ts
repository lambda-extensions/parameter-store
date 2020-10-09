import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import { join, basename } from 'path';
import { existsSync, readFileSync, readSync } from 'fs';

export interface Config {
    compatibleRuntimes: string[];
    src: string;
}

const loadConfig = (path: string): Config => {
    const configPath = join(path, 'config.json');

    if (!(existsSync(configPath))) {
        throw new Error(`unabled to load config.json at path: ${path}`)
    }

    const config = JSON.parse(readFileSync(configPath).toString());
    return config;
}

export interface LayersProps extends cdk.StackProps {
    layerPaths: string[];
}

export class Layers extends cdk.Stack {
    constructor(scope: cdk.Construct, id: string, props: LayersProps) {
        super(scope, id, props);

        props.layerPaths.map(layerPath => {
            const config = loadConfig(layerPath);
            const layerVersionName = basename(layerPath);

            console.log(config)

            const code = lambda.Code.fromAsset(join(layerPath, config.src)).bind(this);

            if (!code.s3Location) {
                throw new Error('Code must define an S3 location');
            }

            const layer = new lambda.CfnLayerVersion(this, layerVersionName, {
                layerName: layerVersionName,
                content: {
                    s3Bucket: code.s3Location.bucketName,
                    s3Key: code.s3Location.objectKey,
                    s3ObjectVersion: code.s3Location.objectVersion
                },
                compatibleRuntimes: config.compatibleRuntimes
            })

            const everyone = '*'
            new lambda.CfnLayerVersionPermission(this, `${layerVersionName}Permission`, {
                layerVersionArn: layer.ref,
                action: 'lambda:GetLayerVersion',
                principal: everyone
            })
        })
    }
}
