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

        certificates = [
            OrderedDict([
                ("name", cert.get("M", {}).get("name", {}).get("S")),
                ("date", cert.get("M", {}).get("date", {}).get("S")),
                ("issuer", cert.get("M", {}).get("issuer", {}).get("S"))
            ]) for cert in resume_data.get("certificates", {}).get("L", [])
        ]

        projects = [
            OrderedDict([
                ("name", proj.get("M", {}).get("name", {}).get("S")),
                ("description", proj.get("M", {}).get("description", {}).get("S")),
                ("highlights", [highlight.get("S") for highlight in proj.get("M", {}).get("highlights", {}).get("L", [])]),
                ("startDate", proj.get("M", {}).get("startDate", {}).get("S")),
                ("endDate", proj.get("M", {}).get("endDate", {}).get("S")),
                ("url", proj.get("M", {}).get("url", {}).get("S"))
            ]) for proj in resume_data.get("projects", {}).get("L", [])
        ]

        skills = [skill.get("S") for skill in resume_data.get("skills", {}).get("L", [])]

        ordered_resume_data = OrderedDict([
            ("id", resume_data.get("id", {}).get("S")),
            ("name", resume_data.get("name", {}).get("M", {}).get("Full Name", {}).get("S")),
            ("basics", basics),
            ("certificates", certificates),
            ("projects", projects),
            ("skills", skills),
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
