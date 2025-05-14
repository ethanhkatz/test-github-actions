import os
import unittest
from unittest.mock import MagicMock, patch

from tpds_lambda_helpers.listener import (  # Replace with the actual module name
    invoke_job_lambda,
    run_listener,
)
from tpds_lambda_helpers.message import Message


class TestListener(unittest.TestCase):

    @patch("tpds_lambda_helpers.listener.safe_call")
    @patch("tpds_lambda_helpers.listener.invoke_job_lambda")
    @patch("tpds_lambda_helpers.listener.DSLogger")
    def test_run_listener_success(
        self, mock_logger, mock_invoke_job_lambda, mock_safe_call
    ):
        """
        Tests successful run of run_listener function
        """

        # Mock successful safe_call
        mock_safe_call.return_value = (True, None)

        # Mock the logger
        mock_logger.info = MagicMock()
        mock_logger.error = MagicMock()

        payload = {
            "Records": [
                {
                    "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
                    "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
                    "body": """{
                "message_id": "123",\
                "service": "Beast",\
                "pipeline": "DSTestPipeline",\
                "job_lambda": "DSTestLambda",\
                "queue_url": "TestQueueURL",\
                "delete_id": null,\
                "init_run_time": 123452401493,\
                "init_run_delay": 5,\
                "job_params": {"param1":"test", "param2":"test2"}\
            }""",
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
                }
            ]
        }

        run_listener(payload)

        mock_logger.info.assert_called_once()
        self.assertIsNone(mock_logger.CONTEXT.get("job_params"))
        mock_logger.error.assert_not_called()

    @patch("tpds_lambda_helpers.listener.safe_call")
    @patch("tpds_lambda_helpers.listener.invoke_job_lambda")
    @patch("tpds_lambda_helpers.listener.DSLogger")
    def test_run_listener_failure(
        self, mock_logger, mock_invoke_job_lambda, mock_safe_call
    ):
        """
        Tests failed run of run_listener function
        """

        # Mock failing safe_call
        mock_safe_call.return_value = (False, Exception("Test Exception"))

        # Mock the logger
        mock_logger.info = MagicMock()
        mock_logger.error = MagicMock()

        payload = {
            "Records": [
                {
                    "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
                    "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
                    "body": """{
                "message_id": "123",\
                "service": "Beast",\
                "pipeline": "DSTestPipeline",\
                "job_lambda": "DSTestLambda",\
                "queue_url": "TestQueueURL",\
                "delete_id": null,\
                "init_run_time": 123452401493,\
                "init_run_delay": 5,\
                "job_params": {"param1":"test", "param2":"test2"}\
            }""",
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
                }
            ]
        }

        run_listener(payload)

        mock_logger.error.assert_called_once()
        mock_logger.info.assert_not_called()

    @patch("tpds_lambda_helpers.listener.boto3.client")
    def test_invoke_job_lambda(self, mock_client):
        """
        Tests invoking job lambda
        """

        # Mock boto3 client
        mock_invoke = mock_client.return_value.invoke
        mock_invoke.return_value = (
            None  # Or whatever you expect the invoke response to be
        )

        msg = Message(
            **{
                "message_id": "123",
                "service": "Beast",
                "pipeline": "DSTestPipeline",
                "job_lambda": "DSTestLambda",
                "queue_url": "TestQueueURL",
                "delete_id": None,
                "init_run_time": 123452401493,
                "init_run_delay": 5,
                "job_params": {"param1": "test", "param2": "test2"},
            }
        )

        invoke_job_lambda(msg)

        # Assert that boto3 client was called with the correct parameters
        mock_client.assert_called_once_with("lambda")
        mock_invoke.assert_called_once()

    @patch("tpds_lambda_helpers.listener.safe_call")
    @patch("tpds_lambda_helpers.listener.invoke_job_lambda")
    @patch("tpds_lambda_helpers.listener.DSLogger")
    def test_run_listener_success_verbose(
        self, mock_logger, mock_invoke_job_lambda, mock_safe_call
    ):
        """
        Tests successful run of run_listener function with verbose logging
        """

        # Mock successful safe_call
        mock_safe_call.return_value = (True, None)

        # Mock the logger
        mock_logger.info = MagicMock()
        mock_logger.error = MagicMock()

        payload = {
            "Records": [
                {
                    "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
                    "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
                    "body": """{
                "message_id": "123",\
                "service": "Beast",\
                "pipeline": "DSTestPipeline",\
                "job_lambda": "DSTestLambda",\
                "queue_url": "TestQueueURL",\
                "delete_id": null,\
                "init_run_time": 123452401493,\
                "init_run_delay": 5,\
                "job_params": {"param1":"test", "param2":"test2"}\
            }""",
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
                }
            ]
        }

        with patch.dict(os.environ, {"LOG_VERBOSE": "True"}):
            run_listener(payload)

        mock_logger.info.assert_called_once()
        self.assertIsNotNone(mock_logger.CONTEXT.get("job_params"))
        mock_logger.error.assert_not_called()
