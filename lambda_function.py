import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):

    #extract s3 event 
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        #get object metadata
        response = s3.head_object(Bucket=bucket, Key=key)
        file_sixe = response['ContentLength']

        #convert to megabytes
        file_size_mb = file_sixe / (1024 * 1024)

        # log alert if file > 100 mb
        if file_size_mb > 1:
            logger.warning(f'Large file detected: {key} - Size: {file_size_mb} MB, exceeds range')
        else:
            logger.info(f'File size: {key} - Size: {file_size_mb} MB, within range ')

    return {
        'statusCode': 200,
        'body': json.dumps('lambda excecuted successfully!')
    }
