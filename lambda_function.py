import json
import boto3
from collections import OrderedDict

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ResumeData')

def lambda_handler(event, context):
    try:
        response = table.get_item(Key={'id': {'S': '1'}})
        resume_data = response.get('Item', {})

        # Function to convert DynamoDB JSON format to standard JSON
        def convert_dynamodb_json(dynamodb_json):
            if isinstance(dynamodb_json, dict):
                if "S" in dynamodb_json:
                    return dynamodb_json["S"]
                elif "M" in dynamodb_json:
                    return {k: convert_dynamodb_json(v) for k, v in dynamodb_json["M"].items()}
                elif "L" in dynamodb_json:
                    return [convert_dynamodb_json(v) for v in dynamodb_json["L"]]
            return dynamodb_json

        standard_json_data = convert_dynamodb_json(resume_data)

        # Create ordered JSON
        ordered_resume_data = OrderedDict([
            ("id", standard_json_data.get("id")),
            ("basics", OrderedDict([
                ("name", standard_json_data["basics"].get("name")),
                ("label", standard_json_data["basics"].get("label")),
                ("email", standard_json_data["basics"].get("email")),
                ("phone", standard_json_data["basics"].get("phone")),
                ("url", standard_json_data["basics"].get("url")),
                ("summary", standard_json_data["basics"].get("summary")),
                ("location", standard_json_data["basics"].get("location")),
                ("profiles", standard_json_data["basics"].get("profiles")),
            ])),
            ("certificates", standard_json_data.get("certificates")),
            ("projects", standard_json_data.get("projects")),
            ("skills", standard_json_data.get("skills")),
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
