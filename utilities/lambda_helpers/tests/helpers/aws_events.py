"""
Example AWS Lambda events. Copied from official AWS Lambda documentation 1/17/23.

https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html
"""

api_gateway_proxy_event = {
    "resource": "/",
    "path": "/",
    "httpMethod": "GET",
    "requestContext": {
        "resourcePath": "/",
        "httpMethod": "GET",
        "path": "/Prod/",
    },
    "headers": {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "Host": "70ixmpl4fl.execute-api.us-east-2.amazonaws.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "X-Amzn-Trace-Id": "Root=1-5e66d96f-7491f09xmpl79d18acf3d050",
    },
    "multiValueHeaders": {
        "accept": [
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        ],
        "accept-encoding": ["gzip, deflate, br"],
    },
    "queryStringParameters": None,
    "multiValueQueryStringParameters": None,
    "pathParameters": {"proxy": "abc123"},
    "stageVariables": None,
    "body": None,
    "isBase64Encoded": False,
}

api_gateway_http_event = {
    "resource": "/",
    "path": "/",
    "httpMethod": "GET",
    "requestContext": {
        "resourcePath": "/",
        "httpMethod": "GET",
        "path": "/Prod/",
        "resourceId": "1234abc",
    },
    "headers": {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "Host": "70ixmpl4fl.execute-api.us-east-2.amazonaws.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "X-Amzn-Trace-Id": "Root=1-5e66d96f-7491f09xmpl79d18acf3d050",
    },
    "multiValueHeaders": {
        "accept": [
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        ],
        "accept-encoding": ["gzip, deflate, br"],
    },
    "queryStringParameters": None,
    "multiValueQueryStringParameters": None,
    "pathParameters": {"http": "get"},
    "stageVariables": None,
    "body": None,
    "isBase64Encoded": False,
}

s3_event = {
    "Records": [
        {
            "eventVersion": "2.1",
            "eventSource": "aws:s3",
            "awsRegion": "us-east-2",
            "eventTime": "2019-09-03T19:37:27.192Z",
            "eventName": "ObjectCreated:Put",
            "userIdentity": {"principalId": "AWS:AIDAINPONIXQXHT3IKHL2"},
            "requestParameters": {"sourceIPAddress": "205.255.255.255"},
            "responseElements": {
                "x-amz-request-id": "D82B88E5F771F645",
                "x-amz-id-2": "vlR7PnpV2Ce81l0PRw6jlUpck7Jo5ZsQjryTjKlc5aLWGVHPZLj5NeC6qMa0emYBDXOo6QBU0Wo=",
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "828aa6fc-f7b5-4305-8584-487c791949c1",
                "bucket": {
                    "name": "DOC-EXAMPLE-BUCKET",
                    "ownerIdentity": {"principalId": "A3I5XTEXAMAI3E"},
                    "arn": "arn:aws:s3:::lambda-artifacts-deafc19498e3f2df",
                },
                "object": {
                    "key": "b21b84d653bb07b05b1e6b33684dc11b",
                    "size": 1305107,
                    "eTag": "b21b84d653bb07b05b1e6b33684dc11b",
                    "sequencer": "0C0F6F405D6ED209E1",
                },
            },
        }
    ]
}

sns_event = {
    "Records": [
        {
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:us-east-2:123456789012:sns-lambda:21be56ed-a058-49f5-8c98-aedd2564c486",
            "EventSource": "aws:sns",
            "Sns": {
                "SignatureVersion": "1",
                "Timestamp": "2019-01-02T12:45:07.000Z",
                "Signature": "tcc6faL2yUC6dgZdmrwh1Y4cGa/ebXEkAi6RibDsvpi+tE/1+82j...65r==",
                "SigningCertUrl": "https://sns.us-east-2.amazonaws.com/SimpleNotificationService-ac565b8b1a6c5d002d285f9598aa1d9b.pem",
                "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                "Message": "Hello from SNS!",
                "MessageAttributes": {
                    "Test": {"Type": "String", "Value": "TestString"},
                    "TestBinary": {"Type": "Binary", "Value": "TestBinary"},
                },
                "Type": "Notification",
                "UnsubscribeUrl": "https://sns.us-east-2.amazonaws.com/?Action=Unsubscribe&amp;SubscriptionArn=arn:aws:sns:us-east-2:123456789012:test-lambda:21be56ed-a058-49f5-8c98-aedd2564c486",
                "TopicArn": "arn:aws:sns:us-east-2:123456789012:sns-lambda",
                "Subject": "TestInvoke",
            },
        }
    ]
}

dynamo_db_event = {
    "Records": [
        {
            "eventID": "1",
            "eventVersion": "1.0",
            "dynamodb": {
                "Keys": {"Id": {"N": "101"}},
                "NewImage": {"Message": {"S": "New item!"}, "Id": {"N": "101"}},
                "StreamViewType": "NEW_AND_OLD_IMAGES",
                "SequenceNumber": "111",
                "SizeBytes": 26,
            },
            "awsRegion": "us-west-2",
            "eventName": "INSERT",
            "eventSourceARN": "arn:aws:dynamodb:us-west-2:111122223333:table/TestTable/stream/2015-05-11T21:21:33.291",
            "eventSource": "aws:dynamodb",
        },
        {
            "eventID": "2",
            "eventVersion": "1.0",
            "dynamodb": {
                "OldImage": {"Message": {"S": "New item!"}, "Id": {"N": "101"}},
                "SequenceNumber": "222",
                "Keys": {"Id": {"N": "101"}},
                "SizeBytes": 59,
                "NewImage": {
                    "Message": {"S": "This item has changed"},
                    "Id": {"N": "101"},
                },
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "awsRegion": "us-west-2",
            "eventName": "MODIFY",
            "eventSourceARN": "arn:aws:dynamodb:us-west-2:111122223333:table/TestTable/stream/2015-05-11T21:21:33.291",
            "eventSource": "aws:dynamodb",
        },
    ]
}

cloudfront_event = {
    "Records": [
        {
            "cf": {
                "config": {"distributionId": "EDFDVBD6EXAMPLE"},
                "request": {
                    "clientIp": "2001:0db8:85a3:0:0:8a2e:0370:7334",
                    "method": "GET",
                    "uri": "/picture.jpg",
                    "headers": {
                        "host": [
                            {"key": "Host", "value": "d111111abcdef8.cloudfront.net"}
                        ],
                        "user-agent": [{"key": "User-Agent", "value": "curl/7.51.0"}],
                    },
                },
            }
        }
    ]
}

scheduled_event_event = {
    "version": "0",
    "account": "123456789012",
    "region": "us-east-2",
    "detail": {},
    "detail-type": "Scheduled Event",
    "source": "aws.events",
    "time": "2019-03-01T01:23:45Z",
    "id": "cdc73f9d-aea9-11e3-9d5a-835b769c0d9c",
    "resources": ["arn:aws:events:us-east-2:123456789012:rule/my-schedule"],
}

cloud_watch_logs_event = {
    "awslogs": {
        "data": "ewogICAgIm1lc3NhZ2VUeXBlIjogIkRBVEFfTUVTU0FHRSIsCiAgICAib3duZXIiOiAiMTIzNDU2Nzg5MDEyIiwKICAgICJsb2dHcm91cCI6I..."
    }
}

aws_config_event = {
    "invokingEvent": '{"configurationItem":{"configurationItemCaptureTime":"2016-02-17T01:36:34.043Z","awsAccountId":"000000000000","configurationItemStatus":"OK","resourceId":"i-00000000","ARN":"arn:aws:ec2:us-east-1:000000000000:instance/i-00000000","awsRegion":"us-east-1","availabilityZone":"us-east-1a","resourceType":"AWS::EC2::Instance","tags":{"Foo":"Bar"},"relationships":[{"resourceId":"eipalloc-00000000","resourceType":"AWS::EC2::EIP","name":"Is attached to ElasticIp"}],"configuration":{"foo":"bar"}},"messageType":"ConfigurationItemChangeNotification"}',
    "ruleParameters": '{"myParameterKey":"myParameterValue"}',
    "resultToken": "myResultToken",
    "eventLeftScope": False,
    "executionRoleArn": "arn:aws:iam::111122223333:role/config-role",
    "configRuleArn": "arn:aws:config:us-east-1:111122223333:config-rule/config-rule-0123456",
    "configRuleName": "change-triggered-config-rule",
    "configRuleId": "config-rule-0123456",
    "accountId": "111122223333",
    "version": "1.0",
}

cloud_formation_event = {
    "RequestType": "Create",
    "ServiceToken": "arn:aws:lambda:us-east-2:123456789012:function:lambda-error-processor-primer-14ROR2T3JKU66",
    "ResponseURL": "https://cloudformation-custom-resource-response-useast2.s3-us-east-2.amazonaws.com/arn%3Aaws%3Acloudformation%3Aus-east-2%3A123456789012%3Astack/lambda-error-processor/1134083a-2608-1e91-9897-022501a2c456%7Cprimerinvoke%7C5d478078-13e9-baf0-464a-7ef285ecc786?AWSAccessKeyId=AKIAIOSFODNN7EXAMPLE&Expires=1555451971&Signature=28UijZePE5I4dvukKQqM%2F9Rf1o4%3D",
    "StackId": "arn:aws:cloudformation:us-east-2:123456789012:stack/lambda-error-processor/1134083a-2608-1e91-9897-022501a2c456",
    "RequestId": "5d478078-13e9-baf0-464a-7ef285ecc786",
    "LogicalResourceId": "primerinvoke",
    "ResourceType": "AWS::CloudFormation::CustomResource",
    "ResourceProperties": {
        "ServiceToken": "arn:aws:lambda:us-east-2:123456789012:function:lambda-error-processor-primer-14ROR2T3JKU66",
        "FunctionName": "lambda-error-processor-randomerror-ZWUC391MQAJK",
    },
}

code_commit_event = {
    "Records": [
        {
            "awsRegion": "us-east-2",
            "codecommit": {
                "references": [
                    {
                        "commit": "5e493c6f3067653f3d04eca608b4901eb227078",
                        "ref": "refs/heads/master",
                    }
                ]
            },
            "eventId": "31ade2c7-f889-47c5-a937-1cf99e2790e9",
            "eventName": "ReferenceChanges",
            "eventPartNumber": 1,
            "eventSource": "aws:codecommit",
            "eventSourceARN": "arn:aws:codecommit:us-east-2:123456789012:lambda-pipeline-repo",
            "eventTime": "2019-03-12T20:58:25.400+0000",
            "eventTotalParts": 1,
            "eventTriggerConfigId": "0d17d6a4-efeb-46f3-b3ab-a63741badeb8",
            "eventTriggerName": "index.handler",
            "eventVersion": "1.0",
            "userIdentityARN": "arn:aws:iam::123456789012:user/intern",
        }
    ]
}

ses_event = {
    "Records": [
        {
            "eventVersion": "1.0",
            "ses": {
                "mail": {
                    "commonHeaders": {
                        "from": ["Jane Doe <janedoe@example.com>"],
                        "to": ["johndoe@example.com"],
                        "returnPath": "janedoe@example.com",
                        "messageId": "<0123456789example.com>",
                        "date": "Wed, 7 Oct 2015 12:34:56 -0700",
                        "subject": "Test Subject",
                    },
                    "source": "janedoe@example.com",
                    "timestamp": "1970-01-01T00:00:00.000Z",
                    "destination": ["johndoe@example.com"],
                    "headers": [
                        {"name": "Return-Path", "value": "<janedoe@example.com>"},
                        {
                            "name": "Received",
                            "value": "from mailer.example.com (mailer.example.com [203.0.113.1]) by inbound-smtp.us-west-2.amazonaws.com with SMTP id o3vrnil0e2ic for johndoe@example.com; Wed, 07 Oct 2015 12:34:56 +0000 (UTC)",
                        },
                        {
                            "name": "DKIM-Signature",
                            "value": "v=1; a=rsa-sha256; c=relaxed/relaxed; d=example.com; s=example; h=mime-version:from:date:message-id:subject:to:content-type; bh=jX3F0bCAI7sIbkHyy3mLYO28ieDQz2R0P8HwQkklFj4=; b=sQwJ+LMe9RjkesGu+vqU56asvMhrLRRYrWCbV",
                        },
                        {"name": "MIME-Version", "value": "1.0"},
                        {"name": "From", "value": "Jane Doe <janedoe@example.com>"},
                        {"name": "Date", "value": "Wed, 7 Oct 2015 12:34:56 -0700"},
                        {"name": "Message-ID", "value": "<0123456789example.com>"},
                        {"name": "Subject", "value": "Test Subject"},
                        {"name": "To", "value": "johndoe@example.com"},
                        {"name": "Content-Type", "value": "text/plain; charset=UTF-8"},
                    ],
                    "headersTruncated": False,
                    "messageId": "o3vrnil0e2ic28tr",
                },
                "receipt": {
                    "recipients": ["johndoe@example.com"],
                    "timestamp": "1970-01-01T00:00:00.000Z",
                    "spamVerdict": {"status": "PASS"},
                    "dkimVerdict": {"status": "PASS"},
                    "processingTimeMillis": 574,
                    "action": {
                        "type": "Lambda",
                        "invocationType": "Event",
                        "functionArn": "arn:aws:lambda:us-west-2:111122223333:function:Example",
                    },
                    "spfVerdict": {"status": "PASS"},
                    "virusVerdict": {"status": "PASS"},
                },
            },
            "eventSource": "aws:ses",
        }
    ]
}

kinesis_event = {
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49590338271490256608559692538361571095921575989136588898",
                "data": "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0Lg==",
                "approximateArrivalTimestamp": 1545084650.987,
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000006:49590338271490256608559692538361571095921575989136588898",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::123456789012:role/lambda-role",
            "awsRegion": "us-east-2",
            "eventSourceARN": "arn:aws:kinesis:us-east-2:123456789012:stream/lambda-stream",
        },
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49590338271490256608559692540925702759324208523137515618",
                "data": "VGhpcyBpcyBvbmx5IGEgdGVzdC4=",
                "approximateArrivalTimestamp": 1545084711.166,
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000006:49590338271490256608559692540925702759324208523137515618",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::123456789012:role/lambda-role",
            "awsRegion": "us-east-2",
            "eventSourceARN": "arn:aws:kinesis:us-east-2:123456789012:stream/lambda-stream",
        },
    ]
}

kinesis_firehose_event = {
    "invocationId": "invoked123",
    "deliveryStreamArn": "aws:lambda:events",
    "region": "us-west-2",
    "records": [
        {
            "data": "SGVsbG8gV29ybGQ=",
            "recordId": "record1",
            "approximateArrivalTimestamp": 1510772160000,
            "kinesisRecordMetadata": {
                "shardId": "shardId-000000000000",
                "partitionKey": "4d1ad2b9-24f8-4b9d-a088-76e9947c317a",
                "approximateArrivalTimestamp": "2012-04-23T18:25:43.511Z",
                "sequenceNumber": "49546986683135544286507457936321625675700192471156785154",
                "subsequenceNumber": "",
            },
        }
    ],
}

kinesis_firehose_event_2 = {
    "invocationId": "invoked123",
    "deliveryStreamArn": "aws:lambda:events",
    "region": "us-west-2",
    "records": [
        {
            "data": "SGVsbG8gV29ybGQ=",
            "recordId": "record1",
            "approximateArrivalTimestamp": 1510772160000,
            "kinesisRecordMetadata": {
                "shardId": "shardId-000000000000",
                "partitionKey": "4d1ad2b9-24f8-4b9d-a088-76e9947c317a",
                "sequenceNumber": "49546986683135544286507457936321625675700192471156785154",
                "subsequenceNumber": "",
            },
        }
    ],
}

cognito_sync_trigger_event = {
    "datasetName": "datasetName",
    "eventType": "SyncTrigger",
    "region": "us-east-1",
    "identityId": "identityId",
    "datasetRecords": {
        "SampleKey2": {
            "newValue": "newValue2",
            "oldValue": "oldValue2",
            "op": "replace",
        },
        "SampleKey1": {
            "newValue": "newValue1",
            "oldValue": "oldValue1",
            "op": "replace",
        },
    },
    "identityPoolId": "identityPoolId",
    "version": 2,
}

sqs_event = {
    "Records": [
        {
            "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
            "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
            "body": "Test message.",
            "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1545082649183",
                "SenderId": "AIDAIENQZJOLO23YVJ4VO",
                "ApproximateFirstReceiveTimestamp": "1545082649185",
            },
            "messageAttributes": {},
            "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:us-east-2:123456789012:my-queue",
            "awsRegion": "us-east-2",
        },
        {
            "messageId": "2e1424d4-f796-459a-8184-9c92662be6da",
            "receiptHandle": "AQEBzWwaftRI0KuVm4tP+/7q1rGgNqicHq...",
            "body": "Test message.",
            "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1545082650636",
                "SenderId": "AIDAIENQZJOLO23YVJ4VO",
                "ApproximateFirstReceiveTimestamp": "1545082650649",
            },
            "messageAttributes": {},
            "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:us-east-2:123456789012:my-queue",
            "awsRegion": "us-east-2",
        },
    ]
}

# A event scheduler is going to come from a lambda invoke originating from a schedule on EventBridge
# It is identified by the presence of the "event_scheduler" key in the event
event_scheduler = {"event_scheduler": "event-name"}

# A lambda event is any dictionary, that is not any other event type
lambda_event = {"not": "another event type"}
