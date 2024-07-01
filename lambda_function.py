import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ResumeData')

def lambda_handler(event, context):
    try:
        response = table.get_item(
            Key={
                'id': '1'
            }
        )
        resume_data = response.get('Item', {})
        formatted_data = convert_dynamodb_to_json(resume_data)
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

def convert_dynamodb_to_json(dynamodb_item):
    def convert_value(value):
        if isinstance(value, dict):
            for key, val in value.items():
                if key == 'S':
                    return val
                elif key == 'N':
                    return int(val) if '.' not in val else float(val)
                elif key == 'M':
                    return convert_dynamodb_to_json(val)
                elif key == 'L':
                    return [convert_value(item) for item in val]
        return value

    return {k: convert_value(v) for k, v in dynamodb_item.items()}
