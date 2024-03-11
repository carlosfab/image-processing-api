
# Image Processing API with AWS

This guide provides step-by-step instructions on how to create and configure an image processing API using AWS API Gateway and Lambda with Python.

![Banner](img/streamlit_app.gif)

## Prerequisites

Before you begin, make sure you have everything you need:

- **Pyenv** - A tool for managing multiple versions of Python. The recommended version of Python for this project is `3.11.3`. To install Pyenv, follow the [Official Pyenv Installation Instructions](https://github.com/pyenv/pyenv#installation).

- **Poetry** - A Python dependency management tool. To install Poetry, follow the [Official Poetry Installation Instructions](https://python-poetry.org/docs/#installation).

- **Docker** - Required for creating an isolated environment that simulates a Lambda function for local testing. To install Docker, follow the instructions at [Install Docker](https://docs.docker.com/). After installation, you can verify if Docker is running with the command `docker ps`.

## Installation and Configuration

Here are the steps you need to follow to set up your development environment:

1. Clone the [Github Repository](https://github.com/carlosfab/image-processing-api) on the `versao-portugues` branch to your local machine and access the `image-processing-api` folder:

   ```bash
   git clone -b versao-portugues https://github.com/carlosfab/image-processing-api.git
   cd image-processing-api
   ```

2. Configure Poetry to create virtual environments within the project directory.

   ```bash
   poetry config virtualenvs.in-project true
   ```

3. Set up the `3.11.3` version of Python with Pyenv:

   ```bash
   pyenv install 3.11.3
   pyenv local 3.11.3
   ```

4. Install project dependencies:

   ```bash
   poetry install
   ```

5. Activate the virtual environment.

   ```bash
   poetry shell
   ```

## Configuring AWS

If you do not already have an AWS account, create an AWS account to be able to use AWS API Gateway and Lambda services. Install and Configure AWS CLI, The AWS CLI is a command-line tool for managing AWS services. Follow the [official instructions to install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

After installation, [configure the AWS CLI with your credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) by running:

   ```bash
   aws configure
   ```

After configuring the AWS CLI, you can obtain your AWS account ID by running the following command:

   ```bash
   aws sts get-caller-identity --query Account --output text
   ```

This command returns your AWS account ID, which is useful for various operations on AWS.

## Docker Image Preparation and Push to ECR

1. **Build Docker Image**

   ```shell
   docker build -t lambda-opencv-image .
   ```

2. **Tag Docker Image**

   ```shell
   docker tag lambda-opencv-image:latest <aws-account-id>.dkr.ecr.<region>.amazonaws.com/lambda-opencv-repo:latest
   ```

3. **Login to ECR**

   ```shell
   aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.<region>.amazonaws.com
   ```

4. **Create Repository in Amazon ECR**

   ```shell
   aws ecr create-repository --repository-name lambda-opencv-repo --region us-east-2
   ```

5. **Push Docker Image to ECR**

   ```shell
   docker push <aws-account-id>.dkr.ecr.<region>.amazonaws.com/lambda-opencv-repo:latest
   ```

## IAM Role Creation for Lambda Execution

1. **Create IAM Role**

   ```shell
   aws iam create-role --role-name LambdaExecutionRole --assume-role-policy-document file://trust-policy.json
   ```

2. **Attach Policy to IAM Role**

   ```shell
   aws iam attach-role-policy --role-name LambdaExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
   ```

## Lambda Function Creation and Configuration

1. **Create Lambda Function Using ECR Image**

   ```shell
   aws lambda create-function      --function-name deskewImage      --package-type Image      --code ImageUri=<aws-account-id>.dkr.ecr.<region>.amazonaws.com/lambda-opencv-repo:latest      --role arn:aws:iam::<aws-account-id>:role/LambdaExecutionRole      --region <region>
   ```

2. **Configure Lambda Function Runtime on Creation**

   ```shell
   aws lambda update-function-configuration --function-name deskewImage --timeout 30 --region <region>
   ```

## Amazon API Gateway API Creation

### API Creation and Configuration

1. **Access Amazon API Gateway**
2. **Create a New API**
3. **Create a New Resource**
4. **Create a POST Method**
5. **Configure the POST Method (Optional)**
6. **Deploy the API**
7. **Test the API**

With these steps, you set up a REST API in Amazon API Gateway, create a POST method to trigger your `deskewImage` Lambda function, and deploy the API for public access.
