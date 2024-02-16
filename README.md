# "OpenAI Assistant Lambda CDK Template"

## What is this?
Have you ever created your own OpenAI Assistant and wanted to get feedback from others?
Indeed, there is a way to set up a reverse proxy in your local development environment to make it accessible from the Internet.
However, there are times when it is difficult to adopt the method of setting up a reverse proxy due to security concerns and restrictions.

This repository's code is a CDK template for deploying a Python app container on AWS Lambda.
Using this repository's code, you can build a demo environment more securely than exposing your local development environment's port to the Internet.


https://github.com/ryohei-kamiya/openai-assistant-lambda-cdk-template/assets/2719533/c58f77c5-73c7-4732-afa2-68866b570c5b


## Requirements
To run the code in this repository, the following conditions must be met:

- You must have an AWS account.
- You must have permission to deploy container applications on Lambda using CDK in your AWS account.
- AWS CDK v2 must be installed in your local development environment.
- You must have an OpenAI API key.
- You must have already created an OpenAI Assistant and have the Assistant ID.

## How to Build the Demo Environment
After cloning this repository, you can build the Assistant's demo environment by executing the following commands.

```sh
$ cp .env.sample .env   # Edit the .env to set OPENAI_API_KEY and OPENAI_ASSISTANT_ID
$ python3 -m pip install -r requirements.txt
$ cdk bootstrap --profile ${YOUR_AWS_PROFILE}
$ cdk deploy --profile ${YOUR_AWS_PROFILE}
```

Upon completion of the `cdk deploy` command, the URL of the demo environment will be displayed on the terminal as the result of the command execution.

## How to Delete the Demo Environment
If the demo environment is no longer needed, it can be deleted by executing the following command.

```sh
$ cdk destroy --profile ${YOUR_AWS_PROFILE}
```
