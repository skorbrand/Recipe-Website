import json
import boto3
import base64
import uuid
import requests
from botocore.exceptions import ClientError

# Initialize DynamoDB and S3 clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

# Define the DynamoDB table name
table_name = 'Recipes'

#Define the S3 bucket name
s3_bucket = 'sydrecipes'

def lambda_handler(event, context):
    try:
        # Generate a new GUID (UUID)
        new_recipe_id = str(uuid.uuid4())

        # Parse the incoming event data
        body = json.loads(event['body'])
        recipe_name = body.get('recipe_name', '')
        cuisine = body.get('cuisine', '')
        time_to_make = body.get('time_to_make', '')
        type_of_food = body.get('type_of_food', '')
        meal_type = body.get('meal_type', '')
        instructions = body.get('instructions', '')
        ingredients = body.get('ingredients', '')
        links = body.get('links', '')
        image_url = body.get('image_url', '')  
        s3_object_key = f'recipe_images/{recipe_name}.jpg'  
        
        response = requests.get(image_url)

        if response.status_code != 200:
            return {
                'statusCode': 400,
                'body': json.dumps('Error: Failed to fetch the image from the provided URL')
            }
        
        # Encode the downloaded image as base64
        image_data = base64.b64encode(response.content).decode('utf-8')

        # Save the image to S3
        s3.put_object(
            Bucket=s3_bucket,
            Key=s3_object_key,
            Body=base64.b64decode(image_data),
            ContentType='image/jpeg'
        )

        # Create a URL to the S3 object
        image_url = f'https://{s3_bucket}.s3.amazonaws.com/{s3_object_key}'

        # Save data to DynamoDB
        table = dynamodb.Table(table_name)
        response = table.put_item(
            Item={
                'recipe_id': new_recipe_id,
                'recipe_name': recipe_name,
                'cuisine': cuisine,
                'image_url': image_url,
                'time_to_make': time_to_make,
                'type_of_food': type_of_food,
                'meal_type': meal_type,
                'instructions': instructions,
                'ingredients': ingredients,
                'links': links
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Recipe and image saved successfully!')
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }