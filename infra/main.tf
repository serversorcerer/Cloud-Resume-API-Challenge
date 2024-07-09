data "aws_iam_role" "existing_lambda_role" {
  name = "iam_for_lambda"
}

resource "aws_iam_role" "iam_for_lambda" {
  count = length(data.aws_iam_role.existing_lambda_role.arn) == 0 ? 1 : 0

  name = "iam_for_lambda"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Effect = "Allow"
      Sid = ""
    }]
  })

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_iam_role_policy" "DynamoDBViewCounterPolicy" {
  name   = "DynamoDBViewCounterPolicy"
  role   = data.aws_iam_role.existing_lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem"
        ]
        Resource = "arn:aws:dynamodb:us-east-1:772529297851:table/cloudresume-test"
      }
    ]
  })

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = data.aws_iam_role.existing_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_lambda_function_url" "url1" {
  function_name      = aws_lambda_function.resume_api.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = ["https://josephaleto.io"]
    allow_methods     = ["*"]
    allow_headers     = ["date", "keep-alive"]
    expose_headers    = ["keep-alive", "date"]
    max_age           = 86400
  }

  lifecycle {
    prevent_destroy = true
  }
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  required_version = ">= 1.0.0"
}

provider "aws" {
  profile = "iamadmin-general"
  region  = "us-east-1"
}

resource "aws_lambda_function" "resume_api" {
  function_name    = "FetchResumeData"
  filename         = "${path.module}/lambda_function.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda_function.zip")
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.8"
  role             = "arn:aws:iam::772529297851:role/service-role/FetchResumeData-role-vzvgg1ft"
  timeout          = 120

  # Temporarily remove prevent_destroy to allow updates
  # lifecycle {
  #   prevent_destroy = true
  # }
}
