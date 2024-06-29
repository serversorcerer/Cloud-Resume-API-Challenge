import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ResumeData')

def lambda_handler(event, context):
    try:
        response = table.get_item(Key={'id': '1'})
        resume_data = response.get('Item', {})
        # Remove AWS-specific attributes from the response
        formatted_data = json.loads(json.dumps(resume_data, default=aws_lambda_default))
        return {
            'statusCode': 200,
            'body': json.dumps(formatted_data, indent=4)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}, indent=4)
        }

def aws_lambda_default(obj):
    if isinstance(obj, dict):
        return {k: aws_lambda_default(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [aws_lambda_default(v) for v in obj]
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    return obj
