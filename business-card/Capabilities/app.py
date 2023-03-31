
from chalice import Chalice, Response
import boto3

app = Chalice(app_name='Capabilities')

@app.route('/business-cards', methods=['POST'])
def extract_info():
    # Create clients for Textract, Comprehend, and DynamoDB
    textract = boto3.client('textract')
    comprehend = boto3.client('comprehend')
    dynamodb = boto3.resource('dynamodb')

    # Upload the image to S3
    s3 = boto3.client('s3')
    bucket_name = 'my-business-card-bucket'
    object_name = 'business-card.jpg'
    s3.upload_file(image, bucket_name, object_name)

    # Analyze the image with Textract
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': object_name
            }
        }
    )

    # Extract the name and email from the Textract response
    name = ''
    email = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'WORD':
            if 'Name' in item['EntityTypes']:
                name += item['Text'] + ' '
            elif 'EmailAddress' in item['EntityTypes']:
                email = item['Text']

    # Analyze the extracted text with Comprehend
    if name and email:
        text = name + email
        sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')['Sentiment']
        entities = comprehend.detect_entities(Text=text, LanguageCode='en')['Entities']
    else:
        sentiment = ''
        entities = []

    # Store the extracted and analyzed data in DynamoDB
    table_name = 'my-business-card-table'
    table = dynamodb.Table(table_name)
    item = {
        'name': name,
        'email': email,
        'sentiment': sentiment,
        'entities': entities
    }
    table.put_item(Item=item)

    # Return the extracted and analyzed information
    return {'name': name.strip(), 'email': email, 'sentiment': sentiment, 'entities': entities}
