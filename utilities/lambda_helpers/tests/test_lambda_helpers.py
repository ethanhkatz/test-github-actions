import unittest

import mock
from tests.helpers.aws_events import *
from tpds_lambda_helpers.lambda_helpers import *
from tpds_lambda_helpers.lambda_helpers import boto3


class SendToSQSTest(unittest.TestCase):

    def test_send_to_sqs_expected(self):
        """
        This will test for when a message id exists in the return value and is not none
        """
        return_value = {"MessageId": "12345"}
        with mock.patch("tpds_lambda_helpers.lambda_helpers.boto3.client") as boto_mock:
            boto_mock.return_value.send_message.return_value = return_value
            self.assertEqual(send_to_sqs("queue_url", "message"), return_value)

    def test_send_to_sqs_message_id_null(self):
        """
        This will test for when a message id exists in the return value but it is none
        """
        return_value = {"MessageId": None}
        with mock.patch("tpds_lambda_helpers.lambda_helpers.boto3.client") as boto_mock:
            boto_mock.return_value.send_message.return_value = return_value
            with self.assertRaises(SQSResponseError):
                send_to_sqs("queue_url", "message")

    def test_send_to_sqs_no_message_id(self):
        """
        This will test for when a message id does not exist in the return value
        """
        return_value = {}
        with mock.patch("tpds_lambda_helpers.lambda_helpers.boto3.client") as boto_mock:
            boto_mock.return_value.send_message.return_value = return_value
            with self.assertRaises(SQSResponseError):
                send_to_sqs("queue_url", "message")


class TestLambdaHelpers(unittest.TestCase):

    def test_is_functions(self):
        """
        Tests individual is functions for event source mapping
        """
        self.assertEqual(
            LambdaEventMapping.is_api_gateway_proxy_event(api_gateway_proxy_event), True
        )
        self.assertEqual(
            LambdaEventMapping.is_api_gateway_http_event(api_gateway_http_event), True
        )
        self.assertEqual(LambdaEventMapping.is_s3_event(s3_event), True)
        self.assertEqual(LambdaEventMapping.is_sns_event(sns_event), True)
        self.assertEqual(LambdaEventMapping.is_dynamo_db_event(dynamo_db_event), True)
        self.assertEqual(LambdaEventMapping.is_cloudfront_event(cloudfront_event), True)
        self.assertEqual(
            LambdaEventMapping.is_scheduled_event(scheduled_event_event), True
        )
        self.assertEqual(
            LambdaEventMapping.is_cloud_watch_logs_event(cloud_watch_logs_event), True
        )
        self.assertEqual(LambdaEventMapping.is_aws_config_event(aws_config_event), True)
        self.assertEqual(
            LambdaEventMapping.is_cloud_formation_event(cloud_formation_event), True
        )
        self.assertEqual(
            LambdaEventMapping.is_code_commit_event(code_commit_event), True
        )
        self.assertEqual(LambdaEventMapping.is_ses_event(ses_event), True)
        self.assertEqual(LambdaEventMapping.is_kinesis_event(kinesis_event), True)
        self.assertEqual(
            LambdaEventMapping.is_kinesis_firehose_event(kinesis_firehose_event), True
        )
        self.assertEqual(
            LambdaEventMapping.is_kinesis_firehose_event(kinesis_firehose_event_2), True
        )
        self.assertEqual(
            LambdaEventMapping.is_cognito_sync_trigger_event(
                cognito_sync_trigger_event
            ),
            True,
        )
        self.assertEqual(LambdaEventMapping.is_sqs_event(sqs_event), True)

    def test_is_event_scheduler_event(self):
        """
        Tests individual is functions
        """
        self.assertEqual(
            LambdaEventMapping.is_event_scheduler_event(event_scheduler), True
        )

    def test_lambda_event_source_valid_events(self):
        """
        Tests high level event source mapping function with valid events
        """
        self.assertEqual(
            LambdaEventMapping.get_lambda_event_source(s3_event), EventMappingEnum.S3
        )
        self.assertEqual(
            LambdaEventMapping.get_lambda_event_source(kinesis_firehose_event_2),
            EventMappingEnum.KINESIS_FIREHOSE,
        )

    def test_lambda_event_event_scheduler(self):
        """
        show that the event scheduler event is mapped to the correct event source
        """
        value = LambdaEventMapping.get_lambda_event_source(event_scheduler)
        self.assertEqual(value, EventMappingEnum.EVENT_SCHEDULER)

    def test_api_gateway_proxy_event(self):
        """
        show that the api gateway proxy event is mapped to the correct event source
        """
        value = LambdaEventMapping.get_lambda_event_source(api_gateway_proxy_event)
        self.assertEqual(value, EventMappingEnum.API_GATEWAY_AWS_PROXY)

    def test_api_gateway_http_event(self):
        """
        show that the api gateway http event is mapped to the correct event source
        """
        value = LambdaEventMapping.get_lambda_event_source(api_gateway_http_event)
        self.assertEqual(value, EventMappingEnum.API_GATEWAY_HTTP)

    def test_sns_event(self):
        """
        show that the sns event is mapped to the correct event source
        """
        value = LambdaEventMapping.get_lambda_event_source(sns_event)
        self.assertEqual(value, EventMappingEnum.SNS)

    def test_dynamo_db_event(self):
        """
        show that the dynamo db event is mapped to the correct event source
        """
        value = LambdaEventMapping.get_lambda_event_source(dynamo_db_event)
        self.assertEqual(value, EventMappingEnum.DYNAMO_DB)

    def test_cloudfront_event(self):
        """
        show that the cloudfront event is mapped to the correct event source
        """
        value = LambdaEventMapping.get_lambda_event_source(cloudfront_event)
        self.assertEqual(value, EventMappingEnum.CLOUDFRONT)

    def test_scheduled_event(self):
        """
        show that the scheduled event is mapped to the correct event source
        """
        value = LambdaEventMapping.get_lambda_event_source(scheduled_event_event)
        self.assertEqual(value, EventMappingEnum.SCHEDULED_EVENT)

    def test_cloud_watch_logs_event(self):
        """
        show that the cloud watch logs event is mapped to the correct event source
        """
        value = LambdaEventMapping.get_lambda_event_source(cloud_watch_logs_event)
        self.assertEqual(value, EventMappingEnum.CLOUD_WATCH_LOGS)

    def test_aws_config_event(self):
        """
        show that the aws config event is mapped to the correct event source
        """
        value = LambdaEventMapping.get_lambda_event_source(aws_config_event)
        self.assertEqual(value, EventMappingEnum.AWS_CONFIG)

    def test_cloud_formation_event(self):
        """
        show that the cloud formation event is mapped to the correct event source
        """
        value = LambdaEventMapping.get_lambda_event_source(cloud_formation_event)
        self.assertEqual(value, EventMappingEnum.CLOUD_FORMATION)

    def test_code_commit_event(self):
        """
        show that the code commit event is mapped to the correct event source
        """
        value = LambdaEventMapping.get_lambda_event_source(code_commit_event)
        self.assertEqual(value, EventMappingEnum.CODE_COMMIT)

    def test_ses_event(self):
        """
        show that the ses event is mapped to the correct event source
        """
        value = LambdaEventMapping.get_lambda_event_source(ses_event)
        self.assertEqual(value, EventMappingEnum.SES)

    def test_kinesis_event(self):
        """
        show that the kinesis event is mapped to the correct event source
        """
        value = LambdaEventMapping.get_lambda_event_source(kinesis_event)
        self.assertEqual(value, EventMappingEnum.KINESIS)

    def test_kinesis_firehose_event(self):
        """
        show that the kinesis firehose event is mapped to the correct event source
        """
        value = LambdaEventMapping.get_lambda_event_source(kinesis_firehose_event)
        self.assertEqual(value, EventMappingEnum.KINESIS_FIREHOSE)

    def test_cognito_sync_trigger_event(self):
        """
        show that the cognito sync trigger event is mapped to the correct event source
        """
        value = LambdaEventMapping.get_lambda_event_source(cognito_sync_trigger_event)
        self.assertEqual(value, EventMappingEnum.COGNITO_SYNC_TRIGGER)

    def test_lambda_event(self):
        """
        show that the lambda event is mapped to the correct event source
        """
        value = LambdaEventMapping.get_lambda_event_source(lambda_event)
        self.assertEqual(value, EventMappingEnum.LAMBDA)

    def test_lambda_event_source_invalid_event(self):
        """
        Tests high level event source mapping function raises NotImplementedError if event not found
        """
        with self.assertRaises(ValueError):
            LambdaEventMapping.get_lambda_event_source("Strings are not valid events")
