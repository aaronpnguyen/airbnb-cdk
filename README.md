
# Setup for CDK projects

Setup required to create and deploy a CDK app:
- Install AWS-CLI
    - Set up config/credential files (AWS resets this every ~12 hours)
- Install CDK
    - Make sure we also have nvm installed, if not, install version 16
    - Within project .venv, make sure we are using nvm 16 [`$ nvm use 16`]

# Getting Started
To create a CDK project, here are the following steps:
1. Create directory and cd into directory
2. Initialize CDK application [`$ cdk init app --language python`]
3. Activate virtual enviornment

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
