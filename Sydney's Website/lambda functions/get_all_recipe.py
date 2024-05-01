import json
import boto3

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Define the DynamoDB table name
table_name = 'Recipes'

def lambda_handler(event, context):
    try:
        # Query DynamoDB for all recipes
        table = dynamodb.Table(table_name)
        response = table.scan()

        # Check if any recipes were found
        if 'Items' in response and len(response['Items']) > 0:
            recipes = response['Items']

            # Construct the response
            recipe_response = [{
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
            } for recipe in recipes]

            return {
                'statusCode': 200,
                'body': json.dumps(recipe_response)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('Recipes not found')
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }