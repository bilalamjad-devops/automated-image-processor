import os
import io
import boto3
from PIL import Image

s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    dest_bucket = os.environ['DESTINATION_BUCKET_NAME']
    sns_arn = os.environ['SNS_TOPIC_ARN']
    resize_ratio = float(os.environ.get('RESIZE_PERCENTAGE', 50)) / 100
    quality = int(os.environ.get('JPEG_QUALITY', 75))

    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        response = s3_client.get_object(Bucket=source_bucket, Key=key)
        image_content = response['Body'].read()

        img = Image.open(io.BytesIO(image_content))

        new_size = (
            int(img.width * resize_ratio),
            int(img.height * resize_ratio)
        )

        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)

        buffer = io.BytesIO()

        resized_img.save(
            buffer,
            format="JPEG",
            quality=quality
        )

        buffer.seek(0)

        new_key = f"resized/{key.split('/')[-1]}"

        s3_client.put_object(
            Bucket=dest_bucket,
            Key=new_key,
            Body=buffer,
            ContentType='image/jpeg'
        )

        message = (
            f"Success! Image '{key}' has been resized "
            f"and uploaded to '{dest_bucket}/{new_key}'."
        )

        sns_client.publish(
            TopicArn=sns_arn,
            Message=message,
            Subject="Image Resizing Success Alert"
        )

    return {
        "statusCode": 200,
        "body": "Image processed successfully!"
    }
