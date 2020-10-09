import * as cdk from '@aws-cdk/core';
import * as iam from '@aws-cdk/aws-iam';
import * as codebuild from '@aws-cdk/aws-codebuild';

export class Ci extends cdk.Stack {
    constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        const appName = `lambda-extensions--parameter-store`

        const prRole = new iam.Role(this, `PrRole`, {
            roleName: `${appName}--pr`,
            assumedBy: new iam.ServicePrincipal('codebuild.amazonaws.com')
        });

        new codebuild.Project(this, `PRs`, {
            projectName: `${appName}--pr`,
            source: codebuild.Source.gitHub({
                repo: 'parameter-store',
                owner: 'lambda-extensions',
                webhook: true,
                webhookFilters: [
                    codebuild.FilterGroup.inEventOf(
                        codebuild.EventAction.PUSH
                    ).andBranchIs('master')
                ],
            }),
            role: prRole,
            environment: {
                buildImage: codebuild.LinuxBuildImage.AMAZON_LINUX_2_3
            }
        })
    }
}
