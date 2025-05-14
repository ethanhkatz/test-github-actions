import uuid
import ast
from datetime import datetime
import json

class Message:
    '''
    Standardized message object for pipeline messaging meaningless change
    '''

    def __init__(self, msg_str=None, **kw) -> None:
        if msg_str: # Convert stringified version of message dictionary to kw dictionary
            kw = self.from_str(msg_str)
        self._message_id = kw.get('message_id') or uuid.uuid4()
        self._service = kw.get('service') or 'Beast'
        self._pipeline = kw.get('pipeline') or ''
        self._job_lambda = kw.get('job_lambda') or ''
        self._queue_url = kw.get('queue_url') or ''
        self._delete_id = kw.get('delete_id') or ''
        self._init_run_time = kw.get('init_run_time') or datetime.now()
        self._init_run_delay = kw.get('init_run_delay') or 0
        self._job_params = kw.get('job_params') or {}

    @property
    def message_id(self) -> str:
        '''
        The Id for the message
        '''
        return self._message_id or ''

    @property
    def service(self) -> str:
        '''
        The architectural tag for the message
        '''
        return self._service or ''

    @property
    def pipeline(self) -> str:
        '''
        The pipeline the message belongs to
        '''
        return self._pipeline or ''

    @property
    def job_lambda(self) -> str:
        '''
        The name of the job lambda function
        '''
        return self._job_lambda or ''

    @property
    def queue_url(self) -> str:
        '''
        The url for the SQS queue
        '''
        return self._queue_url or ''

    @property
    def delete_id(self) -> str:
        '''
        The delete_id for the message on the queue
        '''
        return self._delete_id or ''

    @delete_id.setter
    def delete_id(self, id: str):
        self._delete_id = id

    @property
    def init_run_time(self) -> datetime:
        '''
        The time when the job is first scheduled to run. Will generally be the current time the job was created with any queue delay as an offset
        '''
        return self._init_run_time or datetime.now()

    @property
    def init_run_delay(self) -> int:
        '''
        The time when the job is first scheduled to run. Will generally be the current time the job was created with any queue delay as an offset
        '''
        return self._init_run_delay or 0

    @property
    def job_params(self) -> dict:
        '''
        The parameters for the job to run
        '''
        return self._job_params or {}

    @job_params.setter
    def job_params(self, job_params: dict):
        self._job_params = job_params

    def __str__(self) -> str:
        '''
        Convert Message to string for movement within pipeline
        '''
        return json.dumps(self.to_dict(), default=str)

    def __json__(self) -> dict:
        '''
        Convert to json
        '''
        return self.to_dict()

    def to_dict(self) -> dict:
        '''
        Convert Message to dictionary
        '''
        msg_dict = {
            'message_id': self.message_id,
            'service': self.service,
            'pipeline': self.pipeline,
            'job_lambda': self.job_lambda,
            'queue_url': self.queue_url,
            'delete_id': self.delete_id,
            'init_run_time': self.init_run_time,
            'init_run_delay': self.init_run_delay,
            'job_params': self.job_params
        }
        return msg_dict

    def to_dict_concise(self) -> dict:
        '''
        Converts the Message to a dictionary with only basic elements
        '''
        remove_list = ['queue_url','delete_id','init_run_time','init_run_delay','job_params']
        return {k: v for k, v in self.to_dict().items() if k not in remove_list}


    def from_str(self, msg_str: str) -> dict:
        '''
        Convert Message to kw from string
        '''
        return json.loads(msg_str)
