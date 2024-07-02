import json
import boto3
from collections import OrderedDict
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ResumeData')

def safe_get(d, keys, default=None):
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d

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

        ordered_resume_data = OrderedDict([
            ("id", safe_get(resume_data, ["id", "S"], "")),
            ("name", OrderedDict([
                ("Full Name", safe_get(resume_data, ["basics", "M", "name", "S"], ""))
            ])),
            ("basics", OrderedDict([
                ("summary", safe_get(resume_data, ["basics", "M", "summary", "S"], "")),
                ("phone", safe_get(resume_data, ["basics", "M", "phone", "S"], "")),
                ("email", safe_get(resume_data, ["basics", "M", "email", "S"], "")),
                ("url", safe_get(resume_data, ["basics", "M", "url", "S"], "")),
                ("location", OrderedDict([
                    ("region", safe_get(resume_data, ["basics", "M", "location", "M", "region", "S"], "")),
                    ("city", safe_get(resume_data, ["basics", "M", "location", "M", "city", "S"], "")),
                    ("countryCode", safe_get(resume_data, ["basics", "M", "location", "M", "countryCode", "S"], ""))
                ])),
                ("profiles", [
                    OrderedDict([
                        ("network", safe_get(profile, ["M", "network", "S"], "")),
                        ("username", safe_get(profile, ["M", "username", "S"], "")),
                        ("url", safe_get(profile, ["M", "url", "S"], ""))
                    ]) for profile in safe_get(resume_data, ["basics", "M", "profiles", "L"], [])
                ])
            ])),
            ("certificates", [
                OrderedDict([
                    ("name", safe_get(cert, ["M", "name", "S"], "")),
                    ("date", safe_get(cert, ["M", "date", "S"], "")),
                    ("issuer", safe_get(cert, ["M", "issuer", "S"], ""))
                ]) for cert in safe_get(resume_data, ["certificates", "L"], [])
            ]),
            ("projects", [
                OrderedDict([
                    ("name", safe_get(proj, ["M", "name", "S"], "")),
                    ("description", safe_get(proj, ["M", "description", "S"], "")),
                    ("highlights", [safe_get(highlight, ["S"], "") for highlight in safe_get(proj, ["M", "highlights", "L"], [])]),
                    ("startDate", safe_get(proj, ["M", "startDate", "S"], "")),
                    ("endDate", safe_get(proj, ["M", "endDate", "S"], "")),
                    ("url", safe_get(proj, ["M", "url", "S"], ""))
                ]) for proj in safe_get(resume_data, ["projects", "L"], [])
            ]),
            ("skills", [safe_get(skill, ["S"], "") for skill in safe_get(resume_data, ["skills", "L"], [])])
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
