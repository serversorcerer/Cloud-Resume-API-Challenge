const AWS = require('aws-sdk');

// Initialize AWS DynamoDB client
const dynamodb = new AWS.DynamoDB();

exports.handler = async (event) => {
    // Extract data from event
    const { id, basics, certificates, projects, skills } = event;

    // DynamoDB params for putting an item
    const params = {
        TableName: 'YourTableName', // Replace with your DynamoDB table name
        Item: {
            'id': { S: id },
            'basics': { M: basics },
            'certificates': { L: certificates },
            'projects': { L: projects },
            'skills': { L: skills }
        }
    };

    try {
        // Put item into DynamoDB
        await dynamodb.putItem(params).promise();
        return { statusCode: 200, body: 'Item added successfully' };
    } catch (err) {
        console.error('Error putting item into DynamoDB:', err);
        return { statusCode: 500, body: 'Error putting item into DynamoDB' };
    }
};
