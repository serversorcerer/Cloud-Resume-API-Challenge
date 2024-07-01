import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('YourDynamoDBTableName')

def lambda_handler(event, context):
    response = table.get_item(
        Key={
            'id': '1'
        }
    )
    
    if 'Item' in response:
        item = response['Item']
        result = {
            "id": item["id"]["S"],
            "basics": {
                "name": item["basics"]["M"]["name"]["S"],
                "label": item["basics"]["M"]["label"]["S"],
                "email": item["basics"]["M"]["email"]["S"],
                "phone": item["basics"]["M"]["phone"]["S"],
                "url": item["basics"]["M"]["url"]["S"],
                "summary": item["basics"]["M"]["summary"]["S"],
                "location": {
                    "city": item["basics"]["M"]["location"]["M"]["city"]["S"],
                    "region": item["basics"]["M"]["location"]["M"]["region"]["S"]
                },
                "profiles": [
                    {
                        "network": profile["M"]["network"]["S"],
                        "username": profile["M"]["username"]["S"],
                        "url": profile["M"]["url"]["S"]
                    } for profile in item["basics"]["M"]["profiles"]["L"]
                ]
            },
            "certificates": [
                {
                    "name": certificate["M"]["name"]["S"],
                    "issuer": certificate["M"]["issuer"]["S"],
                    "date": certificate["M"]["date"]["S"]
                } for certificate in item["certificates"]["L"]
            ],
            "projects": [
                {
                    "name": project["M"]["name"]["S"],
                    "startDate": project["M"]["startDate"]["S"],
                    "endDate": project["M"]["endDate"]["S"],
                    "description": project["M"]["description"]["S"],
                    "highlights": [
                        highlight["S"] for highlight in project["M"]["highlights"]["L"]
                    ],
                    "url": project["M"].get("url", {}).get("S", "")
                } for project in item["projects"]["L"]
            ],
            "skills": [skill["S"] for skill in item["skills"]["L"]]
        }
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Item not found'})
        }
