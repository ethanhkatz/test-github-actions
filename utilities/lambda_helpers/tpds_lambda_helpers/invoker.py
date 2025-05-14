from tpds_config.config import safe_call
from .lambda_helpers import send_to_sqs
from tpds_logger.logger import DSLogger
from tpds_env_var.env_var import get_local_env_var
from datetime import datetime
from .message import Message

DSLogger.initialize_to_stdout()

def run_invoker(**kw):
    '''
    Run invoker job (create message, send to sqs, log)
    '''
    # Create message with generated job_params
    msg = create_message(kw.get('service'),
                         kw.get('pipeline'),
                         kw.get('job_lambda'),
                         kw.get('queue_url'),
                         kw.get('msg_delay'),
                         kw.get('job_params'))
    DSLogger.CONTEXT = msg.to_dict()

    # Send message to sqs with delay if need be
    _, value = safe_call(kw.get('queue_url'), str(msg), kw.get('msg_delay') or 0, fn=send_to_sqs, verbose=False)

    # If error, set error values and log msg
    if isinstance(value, Exception):
        return DSLogger.error(message=f"Failure: {value}", stage="Invoker")

    # If success INFO log message (If LOG_VERBOSE is set, log full message, else log concise message)
    verbose = get_local_env_var('LOG', 'VERBOSE')
    if not verbose:
        DSLogger.CONTEXT = msg.to_dict_concise()
    return DSLogger.info(message="Success", stage="Invoker")


def create_message(service, pipeline, job_lambda, queue_url, msg_delay, job_params):
    '''
    Create message object
    '''
    # Build message with supplied job_params
    msg = {
        'message_id': None,
        'service': service,
        'pipeline': pipeline,
        'job_lambda': job_lambda,
        'queue_url': queue_url,
        'delete_id': None,
        'init_run_time': datetime.now(),
        'init_run_delay': msg_delay,
        'job_params': job_params,
    }
    return Message(**msg)
