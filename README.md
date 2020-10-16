# Grouch Auth Function
Serverless function for authenticating to grouch trash service. Uses AWS Secrets manager to validate API Key.

## Build
This project uses sam to build. The following command can be used
```shell script
sam build
```

## Running locally

The function can be ran locally using sam by running the following command
```shell script
sam local start-lambda
```
## Tests
Unit tests can be ran with the following command
```shell script
PYTHONPATH=auth pytest
```

### Cucumber Tests
This project uses Cucumber to automate testing and to describe behavior. To run the tests locally first start the function then run the following command
```shell script
behave -D local 
```

To run the same tests against the production lambda function. First use the `aws configure` command to setup credentials then run
```shell script
behave
``` 

## Deploy
The code will automatically be built and deployed with a [github action.](.github/workflows/build.yml)
To deploy the function manually first use the `aws configure` command to setup credentials for aws, then run
```shell script
sam deploy
```

## Code Scanning
### Snyk OSS Scanning
OSS scanning is done using Snyk as part of the deployment pipeline and results can be viewed on the github action logs. You can run a scan locally by running this command.
```shell script
snyk monitor --file=auth/requirements.txt -- --allow-missing
```

### Sonar Scanning
Sonar quality scans are done as part of the deployment pipeline and results can be viwed on the github action logs. Results can also be found on [Sonarcloud.](https://sonarcloud.io/dashboard?id=grouch-trash-service_grouch-auth-function)
