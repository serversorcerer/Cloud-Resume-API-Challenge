import json
import boto3
from collections import OrderedDict

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ResumeData')

def lambda_handler(event, context):
    try:
        response = table.get_item(Key={'id': '1'})
        resume_data = response.get('Item', {})

        # Reorder the JSON data to match your desired format
        ordered_resume_data = OrderedDict([
            ("id", resume_data.get("id")),
            ("basics", OrderedDict([
                ("name", resume_data["basics"]["M"]["name"]),
                ("label", resume_data["basics"]["M"]["label"]),
                ("email", resume_data["basics"]["M"]["email"]),
                ("phone", resume_data["basics"]["M"]["phone"]),
                ("url", resume_data["basics"]["M"]["url"]),
                ("summary", resume_data["basics"]["M"]["summary"]),
                ("location", OrderedDict([
                    ("city", resume_data["basics"]["M"]["location"]["M"]["city"]),
                    ("region", resume_data["basics"]["M"]["location"]["M"]["region"]),
                ])),
                ("profiles", resume_data["basics"]["M"]["profiles"]),
            ])),
            ("certificates", resume_data.get("certificates")),
            ("projects", resume_data.get("projects")),
            ("skills", resume_data.get("skills")),
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
