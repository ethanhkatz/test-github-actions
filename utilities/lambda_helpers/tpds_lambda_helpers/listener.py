from .message import Message
from tpds_config.config import safe_call
from tpds_logger.logger import DSLogger
from tpds_env_var.env_var import get_local_env_var
from .lambda_helpers import LambdaEventMapping, EventMappingEnum
import boto3
import json

DSLogger.initialize_to_stdout()

def run_listener(event):
    '''
    Runs listener function from supplied event
    '''
    DSLogger.CONTEXT = event

    event_type = LambdaEventMapping.get_lambda_event_source(event)
    if event_type == EventMappingEnum.SQS:
        return run_sqs(event)
    return DSLogger.error(message='Unknown event trigger')

def run_sqs(event):
    '''
    Handles running listener for each job that comes from an SQS invoke
    '''
    records = event.get('Records', [])
    for record in records:
        invoke_sqs(record)
    return {"batchItemFailures": [{"itemIdentifier": ""}]}

def invoke_sqs(record):
    '''
    Creates message and sends to correct job
    '''
    # Create message from payload object
    msg = Message(msg_str=record.get('body'))
    msg.delete_id = record.get('receiptHandle')
    DSLogger.CONTEXT = msg.to_dict()

    # Send message to appropriate function
    _, value = safe_call(msg, fn=invoke_job_lambda, verbose=False)

    # If error, log it and allow message to reappear on queue
    if isinstance(value, Exception):
        return DSLogger.error(message=f"Failure: {value}", stage="Listener")

    # If success log it and allow message to reappear on queue (If LOG_VERBOSE is set, log full message, else log concise message)
    verbose = get_local_env_var('LOG', 'VERBOSE')
    if not verbose:
        DSLogger.CONTEXT = msg.to_dict_concise()
    return DSLogger.info(message="Success", stage="Listener")

def invoke_job_lambda(msg: Message):
    '''
    Invokes job lambda function
    '''
    client = boto3.client('lambda')
    client.invoke(
        FunctionName = msg.job_lambda,
        InvocationType = 'Event',
        Payload = json.dumps(msg.__json__(), default=str).encode('utf-8')
    )
