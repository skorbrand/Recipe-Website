import json
import boto3

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Define the DynamoDB table name and GSI name
table_name = 'Recipes'
index_name = 'recipe_name-index'

def lambda_handler(event, context):
    try:
        # Extract the recipe_name from the query parameters
        recipe_name = event['queryStringParameters']['recipe_name']

        # Query DynamoDB for recipes with the given name using the GSI
        table = dynamodb.Table(table_name)
        response = table.query(
            IndexName=index_name,
            KeyConditionExpression='recipe_name = :name',
            ExpressionAttributeValues={
                ':name': recipe_name
            }
        )

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

    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Missing query parameter: {str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }