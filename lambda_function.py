import json
import boto3
from collections import OrderedDict
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ResumeData')

def convert_dynamodb_json(dynamodb_json):
    if isinstance(dynamodb_json, dict):
        if "S" in dynamodb_json:
            return dynamodb_json["S"]
        elif "M" in dynamodb_json:
            return {k: convert_dynamodb_json(v) for k, v in dynamodb_json["M"].items()}
        elif "L" in dynamodb_json:
            return [convert_dynamodb_json(v) for v in dynamodb_json["L"]]
    return dynamodb_json

def lambda_handler(event, context):
    try:
        response = table.get_item(Key={'id': {'S': '1'}})
        resume_data = response.get('Item', {})

        if not resume_data:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'Item not found'})
            }

        # Convert DynamoDB JSON format to standard JSON format
        standard_json_data = convert_dynamodb_json(resume_data)

        # Create ordered JSON in the specified order
        ordered_resume_data = OrderedDict([
            ("id", standard_json_data.get("id")),
            ("basics", OrderedDict([
                ("name", standard_json_data.get("basics", {}).get("name", "")),
                ("label", standard_json_data.get("basics", {}).get("label", "")),
                ("email", standard_json_data.get("basics", {}).get("email", "")),
                ("phone", standard_json_data.get("basics", {}).get("phone", "")),
                ("url", standard_json_data.get("basics", {}).get("url", "")),
                ("summary", standard_json_data.get("basics", {}).get("summary", "")),
                ("location", OrderedDict([
                    ("city", standard_json_data.get("basics", {}).get("location", {}).get("city", "")),
                    ("region", standard_json_data.get("basics", {}).get("location", {}).get("region", "")),
                    ("countryCode", standard_json_data.get("basics", {}).get("location", {}).get("countryCode", ""))
                ])),
                ("profiles", [
                    OrderedDict([
                        ("network", profile.get("network", "")),
                        ("username", profile.get("username", "")),
                        ("url", profile.get("url", ""))
                    ]) for profile in standard_json_data.get("basics", {}).get("profiles", [])
                ])
            ])),
            ("certificates", [
                OrderedDict([
                    ("name", cert.get("name", "")),
                    ("date", cert.get("date", "")),
                    ("issuer", cert.get("issuer", ""))
                ]) for cert in standard_json_data.get("certificates", [])
            ]),
            ("projects", [
                OrderedDict([
                    ("name", proj.get("name", "")),
                    ("description", proj.get("description", "")),
                    ("highlights", proj.get("highlights", [])),
                    ("startDate", proj.get("startDate", "")),
                    ("endDate", proj.get("endDate", "")),
                    ("url", proj.get("url", ""))
                ]) for proj in standard_json_data.get("projects", [])
            ]),
            ("skills", standard_json_data.get("skills", []))
        ])

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(ordered_resume_data, indent=4)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)}, indent=4)
        }
