import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ResumeData')

def lambda_handler(event, context):
    try:
        response = table.get_item(
            Key={'id': '1'}
        )
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Item not found'})
            }

        resume_data = response['Item']
        
        def convert_ddb_item(item):
            if isinstance(item, dict):
                if 'S' in item:
                    return item['S']
                elif 'N' in item:
                    return item['N']
                elif 'M' in item:
                    return {k: convert_ddb_item(v) for k, v in item['M'].items()}
                elif 'L' in item:
                    return [convert_ddb_item(v) for v in item['L']]
            return item

        formatted_data = convert_ddb_item(resume_data)

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
