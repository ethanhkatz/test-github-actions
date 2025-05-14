import os
import unittest
from unittest.mock import MagicMock, patch

from tpds_lambda_helpers.errors import DeleteError, RetryError
from tpds_lambda_helpers.job import run_job


class TestRunJob(unittest.TestCase):

    @patch("tpds_lambda_helpers.job.safe_call")
    @patch("tpds_lambda_helpers.job.delete_from_sqs")
    @patch("tpds_lambda_helpers.job.DSLogger")
    def test_run_job_success(self, mock_logger, mock_delete_from_sqs, mock_safe_call):
        """
        Tests successful run of run_job function
        """

        # Mock successful safe_call
        mock_safe_call.return_value = (True, None)

        # Mock the logger
        mock_logger.info = MagicMock()
        mock_logger.error = MagicMock()

        # Mock delete_from_sqs
        mock_delete_from_sqs.return_value = None

        event = {
            "message_id": "123",
            "service": "Beast",
            "pipeline": "DSTestPipeline",
            "job_lambda": "DSTestLambda",
            "queue_url": "TestQueueURL",
            "delete_id": "test",
            "init_run_time": 123452401493,
            "init_run_delay": 5,
            "job_params": {"param1": "test", "param2": "test2"},
        }
        job_function = MagicMock()

        run_job(event, job_function)

        mock_logger.info.assert_called_once()
        self.assertIsNone(mock_logger.CONTEXT.get("job_params"))
        mock_logger.error.assert_not_called()
        mock_delete_from_sqs.assert_called_once()

    @patch("tpds_lambda_helpers.job.safe_call")
    @patch("tpds_lambda_helpers.job.delete_from_sqs")
    @patch("tpds_lambda_helpers.job.DSLogger")
    def test_run_job_failure(self, mock_logger, mock_delete_from_sqs, mock_safe_call):
        """
        Tests failed run of run_job function
        """

        # Mock failing safe_call
        mock_safe_call.return_value = (False, Exception("Test Exception"))

        # Mock the logger
        mock_logger.info = MagicMock()
        mock_logger.warning = MagicMock()

        # Mock delete_from_sqs
        mock_delete_from_sqs.return_value = None

        event = {
            "payload": {
                "message_id": "123",
                "service": "Beast",
                "pipeline": "DSTestPipeline",
                "job_lambda": "DSTestLambda",
                "queue_url": "TestQueueURL",
                "delete_id": "test",
                "init_run_time": 123452401493,
                "init_run_delay": 5,
                "job_params": {"param1": "test", "param2": "test2"},
            },
        }
        job_function = MagicMock()

        run_job(event, job_function)

        mock_logger.error.assert_called_once()
        mock_logger.info.assert_not_called()
        mock_delete_from_sqs.assert_not_called()

    @patch("tpds_lambda_helpers.job.delete_from_sqs")
    @patch("tpds_lambda_helpers.job.safe_call")
    @patch("tpds_lambda_helpers.job.DSLogger")
    def test_run_job_retry_error(
        self, mock_logger, mock_safe_call, mock_delete_from_sqs
    ):
        """
        Tests when retry error is raised
        """
        mock_safe_call.return_value = (False, RetryError("Retry error"))
        event = {"payload": {"_message_id": "123"}}
        job_function = MagicMock()
        run_job(event, job_function)
        mock_safe_call.assert_called()
        mock_delete_from_sqs.assert_not_called()
        mock_logger.warning.assert_called_with(
            message="Retry: RetryError(Retry error)", stage="Job"
        )

    @patch("tpds_lambda_helpers.job.delete_from_sqs")
    @patch("tpds_lambda_helpers.job.safe_call")
    @patch("tpds_lambda_helpers.job.DSLogger")
    def test_run_job_delete_error(
        self, mock_logger, mock_safe_call, mock_delete_from_sqs
    ):
        """
        Tests when delete error is raised
        """
        mock_safe_call.return_value = (False, DeleteError("Delete error"))
        event = {"message_id": "123", "delete_id": "test"}
        job_function = MagicMock()
        run_job(event, job_function)
        mock_safe_call.assert_called()
        mock_delete_from_sqs.assert_called_once()
        mock_logger.warning.assert_called_with(
            message="Failure w/ delete: DeleteError(Delete error)", stage="Job"
        )

    @patch("tpds_lambda_helpers.job.safe_call")
    @patch("tpds_lambda_helpers.job.delete_from_sqs")
    @patch("tpds_lambda_helpers.job.DSLogger")
    def test_run_job_success_verbose(
        self, mock_logger, mock_delete_from_sqs, mock_safe_call
    ):
        """
        Tests successful run of run_job function with verbose logging
        """

        # Mock successful safe_call
        mock_safe_call.return_value = (True, None)

        # Mock the logger
        mock_logger.info = MagicMock()
        mock_logger.error = MagicMock()

        # Mock delete_from_sqs
        mock_delete_from_sqs.return_value = None

        event = {
            "message_id": "123",
            "service": "Beast",
            "pipeline": "DSTestPipeline",
            "job_lambda": "DSTestLambda",
            "queue_url": "TestQueueURL",
            "delete_id": "test",
            "init_run_time": 123452401493,
            "init_run_delay": 5,
            "job_params": {"param1": "test", "param2": "test2"},
        }
        job_function = MagicMock()

        with patch.dict(os.environ, {"LOG_VERBOSE": "True"}):
            run_job(event, job_function)

        mock_logger.info.assert_called_once()
        self.assertIsNotNone(mock_logger.CONTEXT.get("job_params"))
        mock_logger.error.assert_not_called()
        mock_delete_from_sqs.assert_called_once()
