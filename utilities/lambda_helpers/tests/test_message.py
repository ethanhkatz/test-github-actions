import json
import unittest

from tpds_lambda_helpers.message import Message


class TestMessage(unittest.TestCase):

    kw = {
        "message_id": "492838210213",
        "service": "Beast",
        "pipeline": "DSTestPipeline",
        "job_lambda": "DSTestLambda",
        "queue_url": "TestQueueURL",
        "delete_id": None,
        "init_run_time": 123452401493,
        "init_run_delay": 5,
        "job_params": {"param1": "test", "param2": "test2"},
    }

    def test_msg_creation(self):
        """
        Test that a message can be created with kw
        """
        msg = Message(**self.kw)
        self.assertEqual(msg.message_id, "492838210213")
        self.assertEqual(msg.service, "Beast")
        self.assertEqual(msg.pipeline, "DSTestPipeline")
        self.assertEqual(msg.job_lambda, "DSTestLambda")
        self.assertEqual(msg.queue_url, "TestQueueURL")
        self.assertEqual(msg.delete_id, "")
        self.assertEqual(msg.init_run_time, 123452401493)
        self.assertEqual(msg.init_run_delay, 5)
        self.assertEqual(msg.job_params, {"param1": "test", "param2": "test2"})

    def test_default_values(self):
        """
        Tests default values are populated
        """
        msg = Message()
        self.assertEqual(msg.service, "Beast")
        self.assertIsNotNone(msg.message_id)

    def test_msg_field_updates(self):
        """
        Test that fields with setters can be updated and those without cannot
        """
        msg = Message(**self.kw)
        msg.delete_id = "abc4321"
        msg.job_params = {"param3": "test3", "param4": "test4"}
        self.assertEqual(msg.delete_id, "abc4321")
        self.assertEqual(msg.job_params, {"param3": "test3", "param4": "test4"})
        with self.assertRaises(
            AttributeError
        ):  # Test that attributes without setters cannot be set
            msg.message_id = "TestUpdate"

    def test_convert_to_string(self):
        """
        Test converting message to a string for placement on queue
        """
        expected_string = '{"message_id": "492838210213", "service": "Beast", "pipeline": "DSTestPipeline", "job_lambda": "DSTestLambda", "queue_url": "TestQueueURL", "delete_id": "", "init_run_time": 123452401493, "init_run_delay": 5, "job_params": {"param1": "test", "param2": "test2"}}'
        msg = Message(**self.kw)
        self.assertEqual(expected_string, str(msg))

    def test_convert_to_dict(self):
        """
        Test converting object to dictionary for logging
        """
        msg = Message(**self.kw)
        expected_dict = {
            "message_id": "492838210213",
            "service": "Beast",
            "pipeline": "DSTestPipeline",
            "job_lambda": "DSTestLambda",
            "queue_url": "TestQueueURL",
            "delete_id": "",
            "init_run_time": 123452401493,
            "init_run_delay": 5,
            "job_params": {"param1": "test", "param2": "test2"},
        }
        self.assertEqual(expected_dict, msg.to_dict())

    def test_create_from_string(self):
        """
        Test creating Message object from stringified version
        """
        str_kw = json.dumps(self.kw)
        msg = Message(msg_str=str_kw)
        self.assertEqual(msg.message_id, "492838210213")
        self.assertEqual(msg.service, "Beast")
        self.assertEqual(msg.pipeline, "DSTestPipeline")
        self.assertEqual(msg.job_lambda, "DSTestLambda")
        self.assertEqual(msg.queue_url, "TestQueueURL")
        self.assertEqual(msg.delete_id, "")
        self.assertEqual(msg.init_run_time, 123452401493)
        self.assertEqual(msg.init_run_delay, 5)
        self.assertEqual(msg.job_params, {"param1": "test", "param2": "test2"})

    def test_convert_to_json(self):
        """
        Tests __json__ magic function to convert to json string
        """
        msg = Message(**self.kw)
        self.assertEqual(msg.to_dict(), msg.__json__())

    def test_basic_dict(self):
        """
        Tests creating basic dictionary for simpler logging
        """
        msg = Message(**self.kw)
        expected_dict = {
            "message_id": "492838210213",
            "service": "Beast",
            "pipeline": "DSTestPipeline",
            "job_lambda": "DSTestLambda",
        }
        self.assertEqual(expected_dict, msg.to_dict_concise())
