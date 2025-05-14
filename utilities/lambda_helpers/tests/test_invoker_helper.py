import os
import unittest

from mock import MagicMock, patch
from tpds_lambda_helpers import invoker


class TestInvoker(unittest.TestCase):

    @patch("tpds_lambda_helpers.invoker.safe_call")
    @patch("tpds_lambda_helpers.invoker.send_to_sqs")
    @patch("tpds_lambda_helpers.invoker.DSLogger")
    def test_run_invoker_success(self, mock_logger, mock_send_to_sqs, mock_safe_call):
        """
        Tests successful run of run_invoker function
        """

        # Mock successful safe_call
        mock_safe_call.return_value = (True, None)

        # Mock the logger
        mock_logger.info = MagicMock()
        mock_logger.error = MagicMock()

        kwargs = {
            "service": "my_service",
            "pipeline": "my_pipeline",
            "job_lambda": "my_lambda",
            "queue_url": "my_queue_url",
            "msg_delay": 5,
            "job_params": {"param1": "test", "param2": "test2"},
        }

        invoker.run_invoker(**kwargs)

        mock_logger.info.assert_called_once()
        self.assertIsNone(mock_logger.CONTEXT.get("job_params"))
        mock_logger.error.assert_not_called()

    @patch("tpds_lambda_helpers.invoker.safe_call")
    @patch("tpds_lambda_helpers.invoker.send_to_sqs")
    @patch("tpds_lambda_helpers.invoker.DSLogger")
    def test_run_invoker_failure(self, mock_logger, mock_send_to_sqs, mock_safe_call):
        """
        Tests failed run of run_invoker function
        """

        # Mock failing safe_call
        mock_safe_call.return_value = (False, Exception("Test Exception"))

        # Mock the logger
        mock_logger.info = MagicMock()
        mock_logger.error = MagicMock()

        kwargs = {
            "service": "my_service",
            "pipeline": "my_pipeline",
            "job_lambda": "my_lambda",
            "queue_url": "my_queue_url",
            "msg_delay": 5,
            "job_params": {"param1": "test", "param2": "test2"},
        }

        invoker.run_invoker(**kwargs)

        mock_logger.error.assert_called_once()
        mock_logger.info.assert_not_called()

    @patch("tpds_lambda_helpers.invoker.safe_call")
    @patch("tpds_lambda_helpers.invoker.send_to_sqs")
    @patch("tpds_lambda_helpers.invoker.DSLogger")
    def test_run_invoker_success_verbose(
        self, mock_logger, mock_send_to_sqs, mock_safe_call
    ):
        """
        Tests successful run of run_invoker function with verbose logging
        """

        # Mock successful safe_call
        mock_safe_call.return_value = (True, None)

        # Mock the logger
        mock_logger.info = MagicMock()
        mock_logger.error = MagicMock()

        kwargs = {
            "service": "my_service",
            "pipeline": "my_pipeline",
            "job_lambda": "my_lambda",
            "queue_url": "my_queue_url",
            "msg_delay": 5,
            "job_params": {"param1": "test", "param2": "test2"},
        }

        with patch.dict(os.environ, {"LOG_VERBOSE": "True"}):
            invoker.run_invoker(**kwargs)

        mock_logger.info.assert_called_once()
        self.assertEqual(mock_logger.CONTEXT.get("job_params"), kwargs["job_params"])
        mock_logger.error.assert_not_called()
