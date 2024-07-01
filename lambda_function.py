import json
import boto3
from collections import OrderedDict

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ResumeData')

def lambda_handler(event, context):
    try:
        response = table.get_item(Key={'id': '1'})
        resume_data = response.get('Item', {})

        ordered_resume_data = OrderedDict([
            ("id", resume_data.get("id")),
            ("basics", resume_data.get("basics")),
            ("certificates", resume_data.get("certificates")),
            ("projects", resume_data.get("projects")),
            ("skills", resume_data.get("skills")),
            ("work", resume_data.get("work"))
        ])

        return {
            'statusCode': 200,
            'body': json.dumps(ordered_resume_data, indent=4)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}, indent=4)
        }
