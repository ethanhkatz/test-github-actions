from .message import Message
from .lambda_helpers import delete_from_sqs
from .errors import RetryError, DeleteError
from tpds_config.config import safe_call
from tpds_logger.logger import DSLogger
from tpds_env_var.env_var import get_local_env_var

DSLogger.initialize_to_stdout()

def run_job(event: dict, job_function):
    '''
    Runs supplied job function with a safe call, logs results.
    '''
    msg = Message(**event)
    DSLogger.CONTEXT = msg.to_dict()

    # Call function with safe call and function params
    _, value = safe_call(**msg.job_params, fn=job_function, verbose=False)

    # If RetryError raised, log warning with retry message
    if isinstance(value, RetryError):
        return DSLogger.warning(message=f"Retry: {value}", stage="Job")

    # If DeleteError raised, log warning and delete message from the queue
    if isinstance(value, DeleteError):
        DSLogger.warning(message=f"Failure w/ delete: {value}", stage="Job")
        return delete_from_sqs(msg.queue_url, msg.delete_id)

    # If general exception raised, log error with message
    if isinstance(value, Exception):
        return DSLogger.error(message=f"Failure: {value}", stage="Job")

    # If no errors, log info and delete message from queue (If LOG_VERBOSE is set, log full message, else log concise message)
    verbose = get_local_env_var('LOG', 'VERBOSE')
    if not verbose:
        DSLogger.CONTEXT = msg.to_dict_concise()
    DSLogger.info(message="Success", stage="Job")
    return delete_from_sqs(msg.queue_url, msg.delete_id)