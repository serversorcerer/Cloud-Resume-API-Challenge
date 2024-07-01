import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ResumeData')

def lambda_handler(event, context):
    try:
        response = table.get_item(Key={'id': '1'})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Item not found'})
            }

        resume_data = response['Item']
        
        # Format the output in the desired order
        formatted_data = {
            "id": resume_data["id"],
            "basics": {
                "name": resume_data["basics"]["name"],
                "label": resume_data["basics"]["label"],
                "email": resume_data["basics"]["email"],
                "phone": resume_data["basics"]["phone"],
                "summary": resume_data["basics"]["summary"],
                "url": resume_data["basics"]["url"],
                "location": {
                    "city": resume_data["basics"]["location"]["city"],
                    "region": resume_data["basics"]["location"]["region"]
                },
                "profiles": resume_data["basics"]["profiles"]
            },
            "skills": resume_data["skills"],
            "projects": resume_data["projects"],
            "certificates": resume_data["certificates"]
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
