'''
Helpers for AWS Lambda functions
'''
from enum import Enum
import boto3

class SQSResponseError(Exception):
    pass

def send_to_sqs(queue_url: str, message_body: str, delay: int=10, message_atr: dict={}) -> dict:
    '''
    Sends message to sqs with supplied message body and message attributes.
    '''
    client = boto3.client('sqs')
    return_value =  client.send_message(
        QueueUrl=queue_url,
        DelaySeconds=delay,
        MessageAttributes=message_atr,
        MessageBody=message_body
    )
    if return_value.get('MessageId'):
        return return_value
    raise SQSResponseError(str(return_value))

def delete_from_sqs(queue_url: str, receipt_handle: str):
    '''
    Deletes message from sqs
    '''
    client = boto3.client('sqs')
    return client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )

class EventMappingEnum(Enum):
    '''
    Enum mappings for event sources
    '''
    EVENT_SCHEDULER = 'event_scheduler'
    API_GATEWAY_AWS_PROXY = 'api_gateway_aws_proxy'
    API_GATEWAY_HTTP = 'api_gateway_http'
    S3 = 's3'
    SNS = 'sns'
    DYNAMO_DB = 'dynamo_db'
    CLOUDFRONT = 'cloudfront'
    SCHEDULED_EVENT = 'scheduled_event'
    CLOUD_WATCH_LOGS = 'cloud_watch_logs'
    AWS_CONFIG = 'aws_config'
    CLOUD_FORMATION = 'cloud_formation'
    CODE_COMMIT = 'code_commit'
    SES = 'ses'
    KINESIS = 'kinesis'
    KINESIS_FIREHOSE = 'kinesis_firehose'
    COGNITO_SYNC_TRIGGER = 'cognito_sync_trigger'
    SQS = 'sqs'


class LambdaEventMapping:
    '''
    Contains functions to assist in mapping Lambda events to the corresponding service source
    '''

    @classmethod
    def get_lambda_event_source(cls, event: dict) -> str:
        '''
        Maps an AWS event to an event source. Raises NotImplementedError when event not found.
        '''
        if cls.is_event_scheduler_event(event):
            return EventMappingEnum.EVENT_SCHEDULER
        if cls.is_api_gateway_proxy_event(event):
            return EventMappingEnum.API_GATEWAY_AWS_PROXY
        if cls.is_api_gateway_http_event(event):
            return EventMappingEnum.API_GATEWAY_HTTP
        if cls.is_s3_event(event):
            return EventMappingEnum.S3
        if cls.is_sns_event(event):
            return EventMappingEnum.SNS
        if cls.is_dynamo_db_event(event):
            return EventMappingEnum.DYNAMO_DB
        if cls.is_cloudfront_event(event):
            return EventMappingEnum.CLOUDFRONT
        if cls.is_scheduled_event(event):
            return EventMappingEnum.SCHEDULED_EVENT
        if cls.is_cloud_watch_logs_event(event):
            return EventMappingEnum.CLOUD_WATCH_LOGS
        if cls.is_aws_config_event(event):
            return EventMappingEnum.AWS_CONFIG
        if cls.is_cloud_formation_event(event):
            return EventMappingEnum.CLOUD_FORMATION
        if cls.is_code_commit_event(event):
            return EventMappingEnum.CODE_COMMIT
        if cls.is_ses_event(event):
            return EventMappingEnum.SES
        if cls.is_kinesis_event(event):
            return EventMappingEnum.KINESIS
        if cls.is_kinesis_firehose_event(event):
            return EventMappingEnum.KINESIS_FIREHOSE
        if cls.is_cognito_sync_trigger_event(event):
            return EventMappingEnum.COGNITO_SYNC_TRIGGER
        if cls.is_sqs_event(event):
            return EventMappingEnum.SQS
        raise NotImplementedError("Event source mapping does not exist")

    @staticmethod
    def is_api_gateway_proxy_event(event: dict) -> bool:
        '''
        Determines if event is api gateway proxy
        '''
        return 'pathParameters' in event and 'proxy' in event['pathParameters']

    @staticmethod
    def is_api_gateway_http_event(event: dict) -> bool:
        '''
        Determines if event is api gateway http
        '''
        return 'requestContext' in event and 'resourceId' in event['requestContext']

    @staticmethod
    def is_s3_event(event: dict) -> bool:
        '''
        Determines if event is s3
        '''
        return 'Records' in event and len(event['Records']) > 0 and 'eventSource' in event['Records'][0] and event['Records'][0]['eventSource'] == 'aws:s3'

    @staticmethod
    def is_sns_event(event: dict) -> bool:
        '''
        Determines if event is sns
        '''
        return 'Records' in event and len(event['Records']) > 0 and 'EventSource' in event['Records'][0] and event['Records'][0]['EventSource'] == 'aws:sns'

    @staticmethod
    def is_dynamo_db_event(event: dict) -> bool:
        '''
        Determines if event is dynamo db
        '''
        return 'Records' in event and len(event['Records']) > 0 and 'eventSource' in event['Records'][0] and event['Records'][0]['eventSource'] == 'aws:dynamodb'

    @staticmethod
    def is_cloudfront_event(event: dict) -> bool:
        '''
        Determines if event is cloudfront
        '''
        return 'Records' in event and len(event['Records']) > 0 and 'cf' in event['Records'][0]

    @staticmethod
    def is_scheduled_event(event: dict) -> bool:
        '''
        Determines if event is scheduled event
        '''
        return 'source' in event and event['source'] == 'aws.events'

    @staticmethod
    def is_cloud_watch_logs_event(event: dict) -> bool:
        '''
        Determines if event is cloud watch logs
        '''
        return 'awslogs' in event and 'data' in event['awslogs']

    @staticmethod
    def is_aws_config_event(event: dict) -> bool:
        '''
        Determines if event is aws config
        '''
        return 'configRuleId' in event and 'configRuleName' in event and 'configRuleArn' in event

    @staticmethod
    def is_cloud_formation_event(event: dict) -> bool:
        '''
        Determines if event is cloudformation
        '''
        return 'StackId' in event and 'RequestType' in event and 'ResourceType' in event

    @staticmethod
    def is_code_commit_event(event: dict) -> bool:
        '''
        Determines if event is code commit
        '''
        return 'Records' in event and len(event['Records']) > 0 and 'eventSource' in event['Records'][0] and event['Records'][0]['eventSource'] == 'aws:codecommit'

    @staticmethod
    def is_ses_event(event: dict) -> bool:
        '''
        Determines if event is ses
        '''
        return 'Records' in event and len(event['Records']) > 0 and 'eventSource' in event['Records'][0] and event['Records'][0]['eventSource'] == 'aws:ses'

    @staticmethod
    def is_kinesis_event(event: dict) -> bool:
        '''
        Determines if event is kinesis
        '''
        return 'Records' in event and len(event['Records']) > 0 and 'eventSource' in event['Records'][0] and event['Records'][0]['eventSource'] == 'aws:kinesis'

    @staticmethod
    def is_kinesis_firehose_event(event: dict) -> bool:
        '''
        Determines if event is kinesis firehose
        '''
        return ('records' in event and len(event['records']) > 0 and 'approximateArrivalTimestamp' in event['records'][0]) or ('records' in event and len(event['records']) > 0 and 'deliveryStreamArn' in event and event['deliveryStreamArn'] is str and event['deliveryStreamArn'].startswith('arn:aws:kinesis:'))

    @staticmethod
    def is_cognito_sync_trigger_event(event: dict) -> bool:
        '''
        Determines if event is cognito sync trigger
        '''
        return 'eventType' in event and event['eventType'] == 'SyncTrigger' and 'identityId' in event and 'identityPoolId' in event

    @staticmethod
    def is_sqs_event(event: dict) -> bool:
        '''
        Determines if event is sqs
        '''
        return 'Records' in event and len(event['Records']) > 0 and 'eventSource' in event['Records'][0] and event['Records'][0]['eventSource'] == 'aws:sqs'
    
    @staticmethod
    def is_event_scheduler_event(event: dict) -> bool:
        '''
        Determines if event is called via event scheduler
        '''
        return 'event_scheduler' in event