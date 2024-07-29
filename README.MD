# Cloud Resume API Challenge

Welcome to the Cloud Resume API Challenge repository! This project showcases my journey and learning experiences with AWS services through the creation of a serverless API to serve my resume data.

## Project Overview

### **AWS Cloud Resume API Challenge**

## Quick Demo

Test the API directly using this curl command:

'''bash
curl https://5yw6uexaub.execute-api.us-east-1.amazonaws.com/Prod/resume 

This project represents a detailed exploration into various AWS services and how they can be utilized to host and manage a serverless API for serving resume data. Below is a summary of the key components and accomplishments of this challenge:

## Key Features

- **Developed a Serverless API**
  - Designed and deployed a RESTful API using AWS Lambda and API Gateway.
  - The API retrieves resume data stored in DynamoDB and returns it in JSON format.

- **Deployed Using AWS Services**
  - Utilized [AWS Lambda](https://aws.amazon.com/lambda/) for running serverless functions.
  - Stored resume data in [DynamoDB](https://aws.amazon.com/dynamodb/), ensuring fast retrieval and high availability.
  - Configured [API Gateway](https://aws.amazon.com/api-gateway/) for secure API access.

- **Automated Deployment with Terraform**
  - Managed AWS resources using [Terraform](https://www.terraform.io/), ensuring Infrastructure as Code practices.
  - Automated resource creation, including Lambda functions, DynamoDB tables, and API Gateway setup.

- **Real-Time Data Handling**
  - Integrated real-time capabilities for fetching the most up-to-date resume data.
  - Implemented efficient querying and data retrieval from DynamoDB.

- **CI/CD Pipeline with GitHub Actions**
  - Set up [GitHub Actions](https://github.com/features/actions) for continuous integration and continuous deployment.
  - Automated updates to the Lambda function and DynamoDB table on code changes.

- **Comprehensive Documentation**
  - Documented the entire API setup and deployment process.
  - Provided insights and methodologies to help others replicate and understand the serverless architecture.

## Getting Started

### Prerequisites

To replicate this project, you'll need the following:

- An [AWS account](https://aws.amazon.com/)
- Familiarity with AWS services such as Lambda, API Gateway, and DynamoDB
- [Terraform](https://www.terraform.io/) installed for infrastructure management
- [GitHub](https://github.com/) account for version control and CI/CD

### Installation and Setup

#### Deploy Infrastructure with Terraform

- Ensure Terraform is installed on your machine.
- Navigate to the `infrastructure` directory and execute:
  ```bash
  terraform init
  terraform apply

#### Deploy the API

- Upload your Lambda function code.
- Configure the API Gateway to expose your Lambda function.

#### Set Up CI/CD with GitHub Actions

- Configure GitHub Actions workflows in the `.github/workflows` directory to automate deployments.

### Usage

Access your API via the API Gateway URL to retrieve your resume in JSON format. Updates to your Lambda function or data will automatically trigger deployments through GitHub Actions.

### Contributing

Contributions are welcome! Feel free to fork the repository, make changes, and submit pull requests. Please ensure your contributions adhere to the project's coding standards and best practices.

### License

This project is licensed under the MIT License. See the LICENSE file for more details.

### Contact

For any questions or inquiries, please reach out to me at joe@josephaleto.io.
