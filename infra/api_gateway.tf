resource "aws_api_gateway_rest_api" "resume_api" {
  name        = "ResumeAPI"
  description = "API for resume data"
}

resource "aws_api_gateway_resource" "resume" {
  rest_api_id = aws_api_gateway_rest_api.resume_api.id
  parent_id   = aws_api_gateway_rest_api.resume_api.root_resource_id
  path_part   = "resume"
}

resource "aws_api_gateway_method" "get_resume" {
  rest_api_id   = aws_api_gateway_rest_api.resume_api.id
  resource_id   = aws_api_gateway_resource.resume.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id             = aws_api_gateway_rest_api.resume_api.id
  resource_id             = aws_api_gateway_resource.resume.id
  http_method             = aws_api_gateway_method.get_resume.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.resume_api.invoke_arn
}

resource "aws_api_gateway_deployment" "deployment" {
  depends_on = [
    aws_api_gateway_integration.lambda,
  ]
  rest_api_id = aws_api_gateway_rest_api.resume_api.id
  stage_name  = "Prod"
}

/*
resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.deployment.id
  rest_api_id   = aws_api_gateway_rest_api.resume_api.id
  stage_name    = "Prod"
}
*/

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.resume_api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:us-east-1:772529297851:5yw6uexaub/*/*/resume"
}

output "api_invoke_url" {
  value = "https://5yw6uexaub.execute-api.us-east-1.amazonaws.com/Prod/resume"
}
