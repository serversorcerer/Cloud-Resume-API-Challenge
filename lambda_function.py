import json
import boto3
from collections import OrderedDict

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ResumeData')

def lambda_handler(event, context):
    try:
        response = table.get_item(Key={'id': '1'})
        resume_data = response.get('Item', {})

        basics = OrderedDict([
            ("email", resume_data.get("basics", {}).get("M", {}).get("email", {}).get("S")),
            ("phone", resume_data.get("basics", {}).get("M", {}).get("phone", {}).get("S")),
            ("url", resume_data.get("basics", {}).get("M", {}).get("url", {}).get("S")),
            ("summary", resume_data.get("basics", {}).get("M", {}).get("summary", {}).get("S")),
            ("location", OrderedDict([
                ("city", resume_data.get("basics", {}).get("M", {}).get("location", {}).get("M", {}).get("city", {}).get("S")),
                ("region", resume_data.get("basics", {}).get("M", {}).get("location", {}).get("M", {}).get("region", {}).get("S")),
                ("countryCode", resume_data.get("basics", {}).get("M", {}).get("location", {}).get("M", {}).get("countryCode", {}).get("S"))
            ])),
            ("profiles", [
                OrderedDict([
                    ("network", profile.get("M", {}).get("network", {}).get("S")),
                    ("username", profile.get("M", {}).get("username", {}).get("S")),
                    ("url", profile.get("M", {}).get("url", {}).get("S"))
                ]) for profile in resume_data.get("basics", {}).get("M", {}).get("profiles", {}).get("L", [])
            ])
        ])

        ordered_resume_data = OrderedDict([
            ("id", resume_data.get("id")),
            ("name", resume_data.get("name")),
            ("basics", basics),
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
