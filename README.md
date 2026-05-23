


# Serverless Automated Image Resizing using AWS Lambda, S3 Buckets and SNS

<img width="1774" height="887" alt="39e41586-5809-46aa-906e-c09d618207a3" src="https://github.com/user-attachments/assets/cba82873-3dfd-4718-bc44-f2ac679a6d85" />




## Project Overview

This project demonstrates an event-driven serverless image processing pipeline on AWS.

Whenever a user uploads an image into an S3 bucket:

- AWS Lambda automatically triggers
- The uploaded image is resized using Python Pillow library
- The resized image is stored in another S3 bucket
- SNS sends an email notification
- CloudWatch logs capture execution details

This project demonstrates modern cloud engineering concepts such as:
- Serverless Computing
- Event-Driven Architecture
- AWS Lambda
- S3 Event Notifications
- SNS Notifications
- Python Boto3 Automation

---

## Problem Statement

Manually resizing uploaded images is repetitive and inefficient for modern cloud applications.

The goal of this project is to automate image processing using AWS serverless services.

This solution automatically:
- detects image uploads
- processes images
- stores resized outputs
- sends notifications
- generates logs for monitoring

without managing servers.

---

## Architecture

```text
User Uploads Image
        ↓
Source S3 Bucket
        ↓
S3 Event Notification
        ↓
AWS Lambda Trigger
        ↓
Resize Image using Pillow
        ↓
Upload to Destination S3 Bucket
        ↓
SNS Email Notification
        ↓
CloudWatch Logs
```

---

## Technologies Used

- AWS Lambda
- AWS S3
- AWS SNS
- AWS CloudWatch
- Python 3.11
- Boto3
- Pillow Library
- Klayers Lambda Layer

---

## Step 1 — Create S3 Buckets

We created two S3 buckets.

#### Source Bucket

Stores original uploaded images.

```text
source-images-bucket-bilalamjad
```


- Bucket name: source-images-bucket
- Keep rest options as it is
- Click create 


<img width="1600" height="900" alt="image-processor - 6" src="https://github.com/user-attachments/assets/3a92d17f-81b4-4539-97a4-0e44683ff7ca" />

<img width="1600" height="900" alt="image-processor - 7" src="https://github.com/user-attachments/assets/a8ef01a0-70c2-48f5-a391-cf6487163991" />

<img width="1600" height="900" alt="image-processor - 8" src="https://github.com/user-attachments/assets/44408087-b515-46a4-90b8-0c00199cd00c" />



#### Destination Bucket

Stores resized images.

```text
resized-images-bucket-bilalamjad
```

- Bucket name: resized-images-bucket
- Keep rest options as it is
- Click create 


<img width="1600" height="900" alt="image-processor - 9" src="https://github.com/user-attachments/assets/d08320f7-186e-49fe-91b8-6e7aa2fc73c4" />

<img width="1600" height="900" alt="image-processor - 10" src="https://github.com/user-attachments/assets/27ec658e-6328-4a89-9706-f429f475bb17" />

<img width="1600" height="900" alt="image-processor - 11" src="https://github.com/user-attachments/assets/ddb5b10b-afad-4cfa-a9f3-1a7b28e54f18" />

<img width="1600" height="900" alt="image-processor - 12" src="https://github.com/user-attachments/assets/b42d140c-40bd-4eaf-8c6b-4e6e13f3038d" />


---

## Step 2 — Create SNS Topic

Create SNS topic:

```text
ImageResizingNotifications
```

Type:
```text
Standard
```

---

#### Create SNS Subscription

Protocol:
```text
Email
```

Endpoint:
```text
your-email@example.com
```

Initially status will show:

```text
Pending confirmation
```

Open your email and confirm subscription.

After confirmation:

```text
Status: Confirmed
```

---

## Step 3 — Create IAM Role for Lambda

Create IAM Role:

```text
ImageResizerLambdaRole
```

Trusted entity:
```text
Lambda
```

Instead of attaching pre-built policies, we created a custom inline policy.

---

## Inline Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::source-images-bucket-bilalamjad/*"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject"],
      "Resource": "arn:aws:s3:::resized-images-bucket-bilalamjad/*"
    },
    {
      "Effect": "Allow",
      "Action": ["sns:Publish"],
      "Resource": "arn:aws:sns:ap-south-1:*:ImageResizingNotifications"
    }
  ]
}
```

> Important:
> Replace bucket names and SNS topic names according to your own environment.

Policy Name:

```text
LambdaCustomS3SNSPolicy
```

---

## Step 4 — Create Lambda Function

Create Lambda function:

```text
ImageResizerFunction
```

Runtime:
```text
Python 3.11
```

Architecture:
```text
arm64
```

Execution role:
```text
ImageResizerLambdaRole
```

---

## Lambda Function Code

```python
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
```

Deploy the function after pasting the code.

---

## Step 5 — Configure Environment Variables

Inside Lambda:

```text
Configuration → Environment Variables
```

Add:

| Key | Value |
|---|---|
| DESTINATION_BUCKET_NAME | resized-images-bucket-bilalamjad |
| SNS_TOPIC_ARN | Your SNS Topic ARN |

---

## Step 6 — Configure Pillow Layer

The Pillow library is required for image resizing.

We used:
- Python 3.11
- arm64 architecture
- Klayers public Lambda layer

---

## Initial Issue

Initially we tried:

```text
arn:aws:lambda:ap-south-1:770693421928:layer:Klayers-p311-pillow:12
```

But received:

```text
Access denied to lambda:GetLayerVersion
```

---

## Root Cause

The selected Klayers version was not compatible with:
- Lambda runtime
- architecture

---

## What is Klayers?

:contentReference[oaicite:0]{index=0}

Klayers is a popular open-source project created by Keith Rozario.

It provides prebuilt AWS Lambda layers for common Python libraries such as:
- Pillow
- Pandas
- Requests

This avoids manually packaging dependencies.

---

## Solution

Update Lambda settings:

Runtime:
```text
Python 3.11
```

Architecture:
```text
arm64
```

Then attach compatible layer:

```text
arn:aws:lambda:ap-south-1:770693421928:layer:Klayers-p311-arm64-Pillow:11
```

Compatible:
- Python 3.11
- arm64

---

## Step 7 — Configure S3 Event Notification

Open source bucket:

```text
source-images-bucket-bilalamjad
```

Navigate:

```text
Properties → Event Notifications
```

Create notification:

| Setting | Value |
|---|---|
| Event Name | TriggerLambdaOnUpload |
| Prefix | Optional |
| Suffix | .jpg |
| Event Type | All Object Create Events |
| Destination | Lambda Function |
| Lambda Function | ImageResizerFunction |

Save changes.

---

## Step 8 — Test the Project

Upload image:

```text
coffee.jpg
```

to:

```text
source-images-bucket-bilalamjad
```

Expected Results:

- Lambda triggers automatically
- Resized image appears in destination bucket
- SNS email notification is received
- CloudWatch logs capture execution details

---

## CloudWatch Logs

Open Lambda function.

Navigate:

```text
Monitor → View CloudWatch Logs
```

You can view:
- log streams
- execution logs
- errors
- Lambda processing details

---

## Cost Optimization

This project uses serverless AWS services which helps minimize infrastructure cost.

#### Cost-saving design choices

- No EC2 servers used
- Lambda only runs when triggered
- SNS pay-per-use model
- S3 low-cost storage
- CloudWatch only stores logs

---

## Cleanup

Delete resources after completing the lab:

- Lambda Function
- IAM Role
- SNS Topic
- S3 Buckets
- CloudWatch Logs

This helps avoid unexpected AWS charges.

---

## Key Learnings

This project helped me understand:

- Event-Driven Architecture
- AWS Lambda automation
- S3 Event Notifications
- SNS email alerts
- Python image processing
- IAM permissions
- Lambda layers
- CloudWatch monitoring
- Serverless cloud design

---

## Future Enhancements

Possible improvements:

- Add PNG and JPEG support
- Generate thumbnails
- Add watermarking
- Store metadata in DynamoDB
- Deploy infrastructure using Terraform
- Add API Gateway upload endpoint
- Add dead-letter queue (DLQ)

---

## Conclusion

This project demonstrates how modern serverless cloud applications can automatically process uploaded files without managing servers.

Using AWS Lambda with S3 events provides:
- scalability
- automation
- low operational overhead
- cost efficiency

This is an excellent beginner-to-intermediate cloud engineering project for learning event-driven serverless architectures.
````
