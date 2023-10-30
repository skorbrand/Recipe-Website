import json
import boto3
from decimal import Decimal

# Initialize DynamoDB and S3 clients
dynamodb = boto3.resource('dynamodb')

# Define the DynamoDB table name
table_name = 'Recipes'
           

def lambda_handler(event, context):
    try:
        # Extract the recipe_id from the request path parameters
        recipe_id = event['pathParameters']['recipe_id']

        # Query DynamoDB for the specific recipe
        table = dynamodb.Table(table_name)
        response = table.get_item(Key={'recipe_id': recipe_id})

        # Check if the recipe exists
        if 'Item' in response:
            recipe = response['Item']




        # Construct the response
            recipe_response = {
                key: float(recipe[key]) if key == 'time_to_make' and recipe[key] is not None else recipe[key]
                for key in [
                    'recipe_id',
                    'recipe_name',
                    'cuisine',
                    'image_url',
                    'time_to_make',
                    'type_of_food',
                    'meal_type',
                    'instructions',
                    'ingredients',
                    'links'
                ]
                if key in recipe and recipe[key]
            }

            return {
                'statusCode': 200,
                'body': json.dumps(recipe_response)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('Recipe not found')
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
