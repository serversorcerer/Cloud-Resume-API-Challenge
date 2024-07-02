import json
import boto3
from collections import OrderedDict
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('resume-api')

def lambda_handler(event, context):
    try:
        response = table.get_item(Key={'id': '1'})
        resume_data = response.get('Item', {})

        if not resume_data:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'Item not found'})
            }
        
        ordered_resume_data = OrderedDict([
            ("id", resume_data.get("id", "")),
            ("name", resume_data.get("name", {})),
            ("basics", resume_data.get("basics", {})),
            ("certificates", resume_data.get("certificates", [])),
            ("projects", resume_data.get("projects", [])),
            ("skills", resume_data.get("skills", [])),
        ])

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(ordered_resume_data, indent=4)
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
