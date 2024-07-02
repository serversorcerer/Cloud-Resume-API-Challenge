import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ResumeData')

def convert_dynamodb_json(data):
    if isinstance(data, dict):
        if 'S' in data:
            return data['S']
        if 'N' in data:
            return data['N']
        if 'M' in data:
            return {k: convert_dynamodb_json(v) for k, v in data['M'].items()}
        if 'L' in data:
            return [convert_dynamodb_json(v) for v in data['L']]
    return data

def lambda_handler(event, context):
    try:
        response = table.get_item(Key={'id': '1'})
        resume_data = response.get('Item', {})

        if not resume_data:
            print("No item found in DynamoDB for the given key '1'")
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'Item not found'})
            }

        converted_data = convert_dynamodb_json(resume_data)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(converted_data, indent=4)
        }
    except ClientError as e:
        print(f"Client error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)}, indent=4)
        }
    except Exception as e:
        print(f"Exception: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)}, indent=4)
        }
