import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ResumeData')

def lambda_handler(event, context):
    try:
        response = table.get_item(
            Key={
                 'id': '1'
            }
        )
        resume_data = response.get('Item', {})
        
        # Reformatting the response
        formatted_data = {
            "id": resume_data["id"]["S"],
            "basics": {
                "name": resume_data["basics"]["M"]["name"]["S"],
                "label": resume_data["basics"]["M"]["label"]["S"],
                "email": resume_data["basics"]["M"]["email"]["S"],
                "phone": resume_data["basics"]["M"]["phone"]["S"],
                "summary": resume_data["basics"]["M"]["summary"]["S"],
                "url": resume_data["basics"]["M"]["url"]["S"],
                "location": {
                    "city": resume_data["basics"]["M"]["location"]["M"]["city"]["S"],
                    "region": resume_data["basics"]["M"]["location"]["M"]["region"]["S"]
                },
                "profiles": [
                    {
                        "network": profile["M"]["network"]["S"],
                        "url": profile["M"]["url"]["S"],
                        "username": profile["M"]["username"]["S"]
                    } for profile in resume_data["basics"]["M"]["profiles"]["L"]
                ]
            },
            "skills": [skill["S"] for skill in resume_data["skills"]["L"]],
            "projects": [
                {
                    "name": project["M"]["name"]["S"],
                    "description": project["M"]["description"]["S"],
                    "highlights": [highlight["S"] for highlight in project["M"]["highlights"]["L"]],
                    "startDate": project["M"]["startDate"]["S"],
                    "endDate": project["M"]["endDate"]["S"]
                } for project in resume_data["projects"]["L"]
            ],
            "certificates": [
                {
                    "name": certificate["M"]["name"]["S"],
                    "date": certificate["M"]["date"]["S"],
                    "issuer": certificate["M"]["issuer"]["S"]
                } for certificate in resume_data["certificates"]["L"]
            ]
        }

        return {
            'statusCode': 200,
            'body': json.dumps(formatted_data, indent=4)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}, indent=4)
        }
