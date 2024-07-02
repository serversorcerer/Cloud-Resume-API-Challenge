import json
import boto3
from collections import OrderedDict

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ResumeData')

def lambda_handler(event, context):
    try:
        response = table.get_item(Key={'id': {'S': '1'}})
        resume_data = response.get('Item', {})

        # Convert DynamoDB JSON format to standard JSON format
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
            ("basics", standard_json_data.get("basics")),
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
