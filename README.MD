# AWS Cloud Resume API Challenge

![AWS Cloud Resume API Challenge Architecture](https://raw.githubusercontent.com/serversorcerer/Cloud-Resume-API-Challenge/main/diagram.png)

Welcome to the repository for my Cloud Resume API Challenge! This project highlights my journey through various AWS services, culminating in the creation of a dynamic, serverless API that serves my resume data. Let's dive into the details of how this was accomplished.

## Quick Demo

Experience the API in action with this curl command:

```sh
curl https://5yw6uexaub.execute-api.us-east-1.amazonaws.com/Prod/resume
```

If you have jq installed, use this for a prettified JSON response:

```sh
curl -X GET https://5yw6uexaub.execute-api.us-east-1.amazonaws.com/Prod/resume | jq .
```



## Overview

This project demonstrates the automated deployment of an AWS Lambda function using Terraform and GitHub Actions. The Lambda function acts as the backend for a resume API, providing endpoints to fetch resume details stored in a DynamoDB table.

## Architecture

The architecture involves:

- **AWS Lambda**: Runs the backend code for the API.
- **AWS API Gateway**: Provides a RESTful API endpoint.
- **DynamoDB**: Stores the json resume data.
- **Terraform**: Manages the infrastructure as code.
- **GitHub Actions**: Automates the CI/CD pipeline.

## Prerequisites

Before getting started, ensure you have the following:

- An AWS account with necessary permissions.
- [Terraform](https://www.terraform.io/downloads.html) installed.
- AWS CLI configured with your credentials.
- A GitHub account with access to the repository.

## Structure of the Project

```plaintext
AWS-CLOUD-RESUME-API/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── infra/
│   ├── .terraform/
│   ├── main.tf
│   ├── provider.tf
│   ├── api_gateway.tf
│   ├── lambda_function.zip
│   ├── requirements.txt
│   └── terraform.tfstate
├── lambda_function/
│   ├── lambda_function.py
│   └── resume_data.json
├── .gitignore
├── LICENSE
├── README.md
```

### Setup Guide 🚀

#### 1. Set Up AWS

- **Sign Up**: Create an AWS account if you don't have one, sign up at [aws.amazon.com](https://aws.amazon.com/).
- **Configure AWS CLI**: Configure your AWS CLI with your credentials using `aws configure`.

#### 2. Create a JSON Resume

- Create a JSON file containing your resume data. Follow a schema [Here](https://jsonresume.org/schema)
- Store this JSON file for later use.

#### 3. Create DynamoDB Table

- **Table Name**: Resumes
- **Primary Key**: `id` (String)
- Populate the table with your resume data using the AWS Management Console, AWS CLI, or a script.

#### 4. Develop the Lambda Function

- Create a Python script (`lambda_function.py`) to fetch resume data from DynamoDB and return it in JSON format.

#### 5. Package the Lambda Function

- Zip the `lambda_function.py` file.

#### 6. Define Infrastructure with Terraform

- Create `main.tf` and `provider.tf` for infrastructure as code as a way to automatically create the lambda function and the API Gateway configurations .

#### 7. Store Terraform State Files

- Create an S3 bucket in the AWS console or the AWS CLI with the same name as the one used in `provider.tf` file .

#### 8. Deploy with Terraform

- **Initialize Terraform**:
  ```sh
  terraform init
  ```
- **Plan the Deployment**:
  ```sh
  terraform plan
  ```
- **Apply Deployment**:
  ```sh
  terraform apply
  ```
- **API Endpoint**: Note the generated API endpoint URL for testing.

#### 9. Automate Github Actions

- **Workflow**: Set up a workflow file in .github/workflows/deploy.yml to automate deployments on code pushes.

#### 10. Test the API

- **Using Curl**: Test the API to ensure it returns resume data in JSON format.
- **Verify CI/CD**: Push changes to GitHub and ensure the GitHub Actions workflow deploys updates correctly.

## Medium Blog

- For a detailed step by step guide to build this project , follow the steps in this [blog]

## Contact

For any questions or inquiries, please reach out to me at joe@josephaleto.io.
