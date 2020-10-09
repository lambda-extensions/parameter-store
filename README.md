# Parameter Store

This is an [AWS Lambda Extension](https://aws.amazon.com/blogs/compute/introducing-aws-lambda-extensions-in-preview/) that allows you to pull values from [SSM Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html).

Supported Runtimes:

|Runtime|Versions|Source|
|-------|--------|------|
|Go|||
|Java|||
|Node.js|||
|Python|3.7, 3.8|[Source](/languages/python)
|Ruby|||

## Usage

### Install the layer

To learn more about the deployment process for this extension, see the [deployment documentation](https://github.com/lambda-extensions/docs).

Add the following arn to your lambda function where `<REGION>` is the region of your function, `LANGAUGE` is your desired language, and `VERSION` is your desired version.

```
arn:aws:lambda:<REGION>:863125196191:layer:<LANGUAGE>-parameter-store-extension:<VERSION>
```

## Contributing

To add a new language implementation, see the [New Language doc](/docs/new-language.md).
