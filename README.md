


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

### Create SNS topic:

```text
ImageResizingNotifications
```

Type:
```text
Standard
```

---

### Create SNS Subscription

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

<img width="1600" height="900" alt="image-processor - 13" src="https://github.com/user-attachments/assets/4e34b30f-a35b-4056-ada5-6345dec88041" />

<img width="1600" height="900" alt="image-processor - 14" src="https://github.com/user-attachments/assets/b7c7d251-9b05-40f4-acaf-02cce1dca011" />

<img width="1600" height="900" alt="image-processor - 15" src="https://github.com/user-attachments/assets/d8af92f1-f8c7-4b97-a46b-ab651fdf65bc" />

<img width="1600" height="900" alt="image-processor - 16" src="https://github.com/user-attachments/assets/7907f104-ca5d-4ef1-a713-7d3b2d404901" />

<img width="1600" height="900" alt="image-processor - 17" src="https://github.com/user-attachments/assets/be91357c-0b86-498a-a374-1d1db9602c0f" />

<img width="1600" height="900" alt="image-processor - 19" src="https://github.com/user-attachments/assets/8f33937f-9bc9-4a38-a044-0ae5065d8ca2" />

<img width="1600" height="900" alt="image-processor - 20" src="https://github.com/user-attachments/assets/805e7d6b-8902-434f-809e-ef0530841814" />

<img width="1600" height="900" alt="image-processor - 21" src="https://github.com/user-attachments/assets/ad335c52-fa28-4426-b4bc-53ded43d75fc" />

<img width="1600" height="900" alt="image-processor - 22" src="https://github.com/user-attachments/assets/bf108ccb-490c-449f-90bd-24d751acb002" />

<img width="1600" height="900" alt="image-processor - 23" src="https://github.com/user-attachments/assets/6087e325-71fb-4ee6-9601-39e2d0e614ad" />

<img width="1600" height="900" alt="image-processor - 24" src="https://github.com/user-attachments/assets/8f3459d7-589a-4878-a990-d990a48e3a75" />

<img width="1600" height="900" alt="image-processor - 25" src="https://github.com/user-attachments/assets/642a7724-fa00-47a7-94e6-1c3ac026640b" />


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


<img width="1600" height="900" alt="image-processor - 26 role" src="https://github.com/user-attachments/assets/a8be7bc6-525e-4ae6-974a-d3727b4ef145" />

<img width="1600" height="900" alt="image-processor - 27" src="https://github.com/user-attachments/assets/454ab81b-128b-4630-9f2a-a3987602b6c7" />

<img width="1600" height="900" alt="image-processor - 28" src="https://github.com/user-attachments/assets/69cc7dfd-aaea-4a05-8d83-7e7a22641eb9" />

<img width="1600" height="900" alt="image-processor - 29" src="https://github.com/user-attachments/assets/a28114a0-8e50-4da0-a7ac-1fb1a984b8c8" />

<img width="1600" height="900" alt="image-processor - 30" src="https://github.com/user-attachments/assets/b5913c2d-c5da-4ae9-8372-08e8e894c1ca" />



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


<img width="1600" height="900" alt="image-processor - 31" src="https://github.com/user-attachments/assets/a66ca714-b0ad-4fd6-b815-79b3dbcb7f19" />

<img width="1600" height="900" alt="image-processor - 32" src="https://github.com/user-attachments/assets/2ba9cdd1-6006-4581-80f1-6c396363cb8b" />

<img width="1600" height="900" alt="image-processor - 33" src="https://github.com/user-attachments/assets/a610f6e3-8f7e-46f1-9503-3fcbf15c3436" />

<img width="1600" height="900" alt="image-processor - 34" src="https://github.com/user-attachments/assets/359ae7b4-eea2-4fa7-bbb9-075b1ef5be41" />

<img width="1600" height="900" alt="image-processor - 35" src="https://github.com/user-attachments/assets/cb4ee73a-00c3-403c-bdf6-51d061a1e21e" />

<img width="1600" height="900" alt="image-processor - 36" src="https://github.com/user-attachments/assets/4d012fc7-7834-4602-a3a2-29565e7968cb" />



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

<img width="1600" height="900" alt="image-processor - 36b" src="https://github.com/user-attachments/assets/c673b029-a53d-41bc-8d46-001d2978f9a5" />

<img width="1600" height="900" alt="image-processor - 37" src="https://github.com/user-attachments/assets/f0693ca2-a641-448d-8e76-f196c593d65a" />

<img width="1600" height="900" alt="image-processor - 38" src="https://github.com/user-attachments/assets/51d0d0a0-8692-4e6a-9f57-72376b8aec81" />

<img width="1600" height="900" alt="image-processor - 39" src="https://github.com/user-attachments/assets/38126ee9-27bd-41e4-8460-ef244df69509" />

<img width="1600" height="900" alt="image-processor - 41" src="https://github.com/user-attachments/assets/e2b5ba86-2943-4cfc-ae6a-88f77c00b054" />

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


<img width="1600" height="900" alt="image-processor - 42" src="https://github.com/user-attachments/assets/a0b984f6-b209-444c-ab12-6f09ee8c5a4f" />

<img width="1600" height="900" alt="image-processor - 43" src="https://github.com/user-attachments/assets/dc910cc0-1069-4881-811e-481ef466eb61" />


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


<img width="1600" height="900" alt="image-processor - 44" src="https://github.com/user-attachments/assets/be82bc0b-a8af-41c1-a54c-8e05a391d2a3" />

<img width="1600" height="900" alt="image-processor - 45" src="https://github.com/user-attachments/assets/f25e9cc1-5206-41c1-8457-14e29b0601bd" />

<img width="1600" height="900" alt="image-processor - 46" src="https://github.com/user-attachments/assets/33851f1a-8c6b-4f69-8a56-09bf6e72cf30" />

<img width="1600" height="900" alt="image-processor - 47" src="https://github.com/user-attachments/assets/deb02efc-33e0-42a7-978f-fe992a0b750f" />

<img width="1600" height="900" alt="image-processor - 48" src="https://github.com/user-attachments/assets/91b807f5-f288-49ad-885c-a43a9342ea67" />


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


<img width="1600" height="900" alt="image-processor - 49" src="https://github.com/user-attachments/assets/c9e71132-660d-45c5-ab1a-44d59925e880" />

<img width="1600" height="900" alt="image-processor - 50" src="https://github.com/user-attachments/assets/ebe5febf-9f37-43ac-8cae-fb79a3554604" />

<img width="1600" height="900" alt="image-processor - 73" src="https://github.com/user-attachments/assets/a56a10a5-8409-42e3-a400-d1fda4ab38df" />

---

<img width="1600" height="900" alt="image-processor - 57" src="https://github.com/user-attachments/assets/dfa83cc5-b669-4a3c-a2ee-950f4c63fcf2" />

<img width="1600" height="900" alt="image-processor - 58" src="https://github.com/user-attachments/assets/f05de839-9905-4f83-ba3e-92d12f63fd20" />

<img width="1600" height="900" alt="image-processor - 80" src="https://github.com/user-attachments/assets/1fec251e-dc4a-409f-a8b4-c96583a8cb09" />

<img width="1600" height="900" alt="image-processor - 81" src="https://github.com/user-attachments/assets/b60d50b1-3ec4-4721-87ce-e569add7e2e0" />

---

<img width="1600" height="900" alt="image-processor - 82" src="https://github.com/user-attachments/assets/38a7a125-fe9b-4886-9d8d-6b023e258708" />

<img width="1600" height="900" alt="image-processor - 83" src="https://github.com/user-attachments/assets/0519f0f2-12d5-476a-8406-8b5301d82c54" />

<img width="1600" height="900" alt="image-processor - 84" src="https://github.com/user-attachments/assets/51a06bd4-b624-4fdd-9178-dd1294e534a8" />

<img width="1600" height="900" alt="image-processor - 85" src="https://github.com/user-attachments/assets/b380bd17-8ca9-4688-9211-9869aa35fd4c" />

<img width="1600" height="900" alt="image-processor - 86" src="https://github.com/user-attachments/assets/392917e2-9c9f-4a12-bc88-3cfdb7f620f5" />



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
