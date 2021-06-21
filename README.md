# aws-s3-lambda

[![Build Status](https://travis-ci.com/geek-kb/aws-s3-lambda.svg?branch=main)](https://travis-ci.com/geek-kb/aws-s3-lambda)

This repository contains a code that configures a "container image" AWS lambda function that is triggerred automatically when a file is uploaded to a bucket.

In order to test it, the following should be configured:

1. Create a s3 bucket.
2. Configure the following bucket policy in the bucket created in the previous step:

```
{
    "Version": "2012-10-17",
    "Id": "ExamplePolicy",
    "Statement": [
        {
            "Sid": "s3-bucket-policy",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME"
            },
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::BUCKET_NAME",
                "arn:aws:s3:::BUCKET_NAME/*"
            ]
        }
    ]
}
```
3. Create a new IAM user/role.
4. Configure the following IAM policies:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3BucketPermissions",
            "Action": [
                "s3:GetObject",
                "s3:ListObjects",
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::BUCKET_NAME/*",
                "arn:aws:s3:::BUCKET_NAME"
            ]
        }
    ]
}
```

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "SesSendEmailPermissions",
            "Effect": "Allow",
            "Action": [
                "ses:SendEmail",
                "ses:SendRawEmail"
            ],
            "Resource": "*"
        }
    ]
}
```

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EcrUploadPermission",
            "Effect": "Allow",
            "Action": [
                "ecr:BatchGetImage",
                "ecr:BatchCheckLayerAvailability",
                "ecr:CompleteLayerUpload",
                "ecr:DescribeImages",
                "ecr:DescribeRepositories",
                "ecr:GetDownloadUrlForLayer",
                "ecr:InitiateLayerUpload",
                "ecr:ListImages",
                "ecr:PutImage",
                "ecr:UploadLayerPart"
            ],
            "Resource": "arn:aws:ecr:${AWS_REGION}:${AWS_ACCOUNT_ID}:repository/${ECR_REPO_NAME}"
        },
        {
            "Effect": "Allow",
            "Action": "ecr:GetAuthorizationToken",
            "Resource": "*"
        }
    ]
}
```

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "LambdaUpdatePermissions",
            "Action": [
                "lambda:UpdateFunctionCode"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:lambda:${AWS_REGION}:${AWS_ACCOUNT_ID}:function:${LAMBDA_FUNCTION_NAME}"
            ]
        }
    ]
}
```
5. Attach the policy "AWSLambdaBasicExecutionRole" and the above policies to the IAM user/role you created.
6. Create a new lambda function and choose "Use a blueprint", check the "s3-get-object-python" option.
7. Name the function, Under execution role choose "Use an existing role" and use the role created in step 3.
8. Under S3 Trigger, choose the bucket you created in step 1 and click "Create Function".
9. Edit the function, choose "Environment variables" on the left pane and create the following variables and set their values:

* email_address
* region
* user_name

10. Go to AWS SES and in the left panel, under Identity management click "Email addresses".
11. Click the "Verify a new email address" and enter the email address you want the function to use when it notifies on newly created objects in the S3 bucket it watches.
12. Open your email account, find the verification email sent by SES and approve the email address.
13. Upload a file to the bucket to test the lambda function trigger.
