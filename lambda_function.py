import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ResumeData')

def lambda_handler(event, context):
    try:
        response = table.get_item(Key={'id': '1'})
        resume_data = response.get('Item', {})
        
        ordered_resume_data = {
            'id': resume_data.get('id', {}).get('S', ''),
            'basics': {
                'name': resume_data.get('basics', {}).get('M', {}).get('name', {}).get('S', ''),
                'label': resume_data.get('basics', {}).get('M', {}).get('label', {}).get('S', ''),
                'email': resume_data.get('basics', {}).get('M', {}).get('email', {}).get('S', ''),
                'phone': resume_data.get('basics', {}).get('M', {}).get('phone', {}).get('S', ''),
                'location': {
                    'city': resume_data.get('basics', {}).get('M', {}).get('location', {}).get('M', {}).get('city', {}).get('S', ''),
                    'region': resume_data.get('basics', {}).get('M', {}).get('location', {}).get('M', {}).get('region', {}).get('S', ''),
                },
                'profiles': [
                    {
                        'network': resume_data.get('basics', {}).get('M', {}).get('profiles', {}).get('L', [])[0].get('M', {}).get('network', {}).get('S', ''),
                        'url': resume_data.get('basics', {}).get('M', {}).get('profiles', {}).get('L', [])[0].get('M', {}).get('url', {}).get('S', ''),
                        'username': resume_data.get('basics', {}).get('M', {}).get('profiles', {}).get('L', [])[0].get('M', {}).get('username', {}).get('S', ''),
                    },
                    {
                        'network': resume_data.get('basics', {}).get('M', {}).get('profiles', {}).get('L', [])[1].get('M', {}).get('network', {}).get('S', ''),
                        'url': resume_data.get('basics', {}).get('M', {}).get('profiles', {}).get('L', [])[1].get('M', {}).get('url', {}).get('S', ''),
                        'username': resume_data.get('basics', {}).get('M', {}).get('profiles', {}).get('L', [])[1].get('M', {}).get('username', {}).get('S', ''),
                    },
                    {
                        'network': resume_data.get('basics', {}).get('M', {}).get('profiles', {}).get('L', [])[2].get('M', {}).get('network', {}).get('S', ''),
                        'url': resume_data.get('basics', {}).get('M', {}).get('profiles', {}).get('L', [])[2].get('M', {}).get('url', {}).get('S', ''),
                        'username': resume_data.get('basics', {}).get('M', {}).get('profiles', {}).get('L', [])[2].get('M', {}).get('username', {}).get('S', ''),
                    },
                ],
                'summary': resume_data.get('basics', {}).get('M', {}).get('summary', {}).get('S', ''),
                'url': resume_data.get('basics', {}).get('M', {}).get('url', {}).get('S', ''),
            },
            'certificates': [
                {
                    'name': resume_data.get('certificates', {}).get('L', [])[0].get('M', {}).get('name', {}).get('S', ''),
                    'date': resume_data.get('certificates', {}).get('L', [])[0].get('M', {}).get('date', {}).get('S', ''),
                    'issuer': resume_data.get('certificates', {}).get('L', [])[0].get('M', {}).get('issuer', {}).get('S', ''),
                },
                {
                    'name': resume_data.get('certificates', {}).get('L', [])[1].get('M', {}).get('name', {}).get('S', ''),
                    'date': resume_data.get('certificates', {}).get('L', [])[1].get('M', {}).get('date', {}).get('S', ''),
                    'issuer': resume_data.get('certificates', {}).get('L', [])[1].get('M', {}).get('issuer', {}).get('S', ''),
                },
            ],
            'projects': [
                {
                    'name': resume_data.get('projects', {}).get('L', [])[0].get('M', {}).get('name', {}).get('S', ''),
                    'description': resume_data.get('projects', {}).get('L', [])[0].get('M', {}).get('description', {}).get('S', ''),
                    'startDate': resume_data.get('projects', {}).get('L', [])[0].get('M', {}).get('startDate', {}).get('S', ''),
                    'endDate': resume_data.get('projects', {}).get('L', [])[0].get('M', {}).get('endDate', {}).get('S', ''),
                    'highlights': [
                        resume_data.get('projects', {}).get('L', [])[0].get('M', {}).get('highlights', {}).get('L', [])[0].get('S', ''),
                        resume_data.get('projects', {}).get('L', [])[0].get('M', {}).get('highlights', {}).get('L', [])[1].get('S', ''),
                        resume_data.get('projects', {}).get('L', [])[0].get('M', {}).get('highlights', {}).get('L', [])[2].get('S', ''),
                    ],
                    'url': resume_data.get('projects', {}).get('L', [])[0].get('M', {}).get('url', {}).get('S', ''),
                },
                {
                    'name': resume_data.get('projects', {}).get('L', [])[1].get('M', {}).get('name', {}).get('S', ''),
                    'description': resume_data.get('projects', {}).get('L', [])[1].get('M', {}).get('description', {}).get('S', ''),
                    'startDate': resume_data.get('projects', {}).get('L', [])[1].get('M', {}).get('startDate', {}).get('S', ''),
                    'endDate': resume_data.get('projects', {}).get('L', [])[1].get('M', {}).get('endDate', {}).get('S', ''),
                    'highlights': [
                        resume_data.get('projects', {}).get('L', [])[1].get('M', {}).get('highlights', {}).get('L', [])[0].get('S', ''),
                        resume_data.get('projects', {}).get('L', [])[1].get('M', {}).get('highlights', {}).get('L', [])[1].get('S', ''),
                        resume_data.get('projects', {}).get('L', [])[1].get('M', {}).get('highlights', {}).get('L', [])[2].get('S', ''),
                        resume_data.get('projects', {}).get('L', [])[1].get('M', {}).get('highlights', {}).get('L', [])[3].get('S', ''),
                    ],
                    'url': resume_data.get('projects', {}).get('L', [])[1].get('M', {}).get('url', {}).get('S', ''),
                },
            ],
            'skills': [
                {'name': skill.get('S', '')} for skill in resume_data.get('skills', {}).get('L', [])
            ],
        }

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
