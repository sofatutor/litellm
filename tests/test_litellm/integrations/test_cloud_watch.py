import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import pytest

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from litellm.integrations.cloud_watch import CloudWatchLogger


class TestCloudWatchLogger(unittest.TestCase):
    """
    Tests for the CloudWatch Logger integration
    """

    def setUp(self):
        """Set up test fixtures"""
        # Set AWS region for testing
        self.aws_region = "us-west-2"
        
        # Create a log group and stream name for testing
        self.log_group_name = "test-log-group"
        self.log_stream_name = "test-log-stream"
        
        # Create a patch for litellm module
        self.litellm_patcher = patch("litellm.integrations.cloud_watch.litellm")
        self.mock_litellm = self.litellm_patcher.start()
        self.mock_litellm.cloudwatch_callback_params = None
        self.mock_litellm.get_secret = lambda x: x.replace("os.environ/", "")

    def tearDown(self):
        """Clean up after tests"""
        self.litellm_patcher.stop()

    @patch("litellm.integrations.cloud_watch.boto3")
    def test_init(self, mock_boto3):
        """Test CloudWatchLogger initialization"""
        # Arrange
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client
        
        # Act
        logger = CloudWatchLogger(
            log_group_name=self.log_group_name,
            log_stream_name=self.log_stream_name,
            aws_region=self.aws_region,
        )
        
        # Assert
        mock_boto3.client.assert_called_once_with(
            "logs",
            region_name=self.aws_region,
        )
        
        assert logger.log_group_name == self.log_group_name
        assert logger.log_stream_name == self.log_stream_name

    @patch("litellm.integrations.cloud_watch.boto3")
    def test_init_with_callback_params(self, mock_boto3):
        """Test CloudWatchLogger initialization with callback params"""
        # Arrange
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client
        
        # Set callback params
        self.mock_litellm.cloudwatch_callback_params = {
            "log_group_name": "callback-group",
            "log_stream_name": "callback-stream",
            "aws_region": "us-east-1",
        }
        
        # Act
        logger = CloudWatchLogger()
        
        # Assert
        mock_boto3.client.assert_called_once_with(
            "logs",
            region_name="us-east-1",
        )
        
        assert logger.log_group_name == "callback-group"
        assert logger.log_stream_name == "callback-stream"

    @patch("litellm.integrations.cloud_watch.boto3")
    def test_log_success_event(self, mock_boto3):
        """Test logging a successful event to CloudWatch"""
        # Arrange
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client
        
        logger = CloudWatchLogger(
            log_group_name=self.log_group_name,
            log_stream_name=self.log_stream_name,
            aws_region=self.aws_region,
        )
        
        # Create test data
        test_kwargs = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Hello"}],
            "litellm_params": {
                "metadata": {
                    "call_type": "completion", 
                    "litellm_call_id": "test-call-id",
                }
            }
        }
        
        test_response = {
            "model": "gpt-4",
            "choices": [
                {
                    "message": {"role": "assistant", "content": "Hi there!"},
                    "finish_reason": "stop",
                    "index": 0,
                }
            ],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        }
        
        # Act
        logger.log_event(
            kwargs=test_kwargs,
            response_obj=test_response,
            start_time=1234567890,
            end_time=1234567895,
            print_verbose=lambda x: None,
        )
        
        # Assert
        # Verify log events was called
        mock_client.put_log_events.assert_called_once()
        
        # Extract the call arguments
        call_args = mock_client.put_log_events.call_args[1]
        
        # Verify log group and stream
        assert call_args["logGroupName"] == self.log_group_name
        assert call_args["logStreamName"] == self.log_stream_name
        
        # Verify log events contains data
        log_events = call_args["logEvents"]
        assert len(log_events) == 1
        
        # Verify timestamp is present
        assert "timestamp" in log_events[0]

    @patch("litellm.integrations.cloud_watch.boto3")
    def test_log_failure_event(self, mock_boto3):
        """Test logging a failure event to CloudWatch"""
        # Arrange
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client
        
        logger = CloudWatchLogger(
            log_group_name=self.log_group_name,
            log_stream_name=self.log_stream_name,
            aws_region=self.aws_region,
        )
        
        # Create test data
        test_kwargs = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Hello"}],
            "litellm_params": {
                "metadata": {
                    "call_type": "completion",
                    "litellm_call_id": "test-call-id",
                    "error": "API rate limit exceeded"
                }
            }
        }
        
        # Act
        logger.log_event(
            kwargs=test_kwargs,
            response_obj=None,
            start_time=1234567890,
            end_time=1234567895,
            print_verbose=lambda x: None,
        )
        
        # Assert
        # Verify put_log_events was called
        mock_client.put_log_events.assert_called_once()

# For pytest compatibility
def test_cloudwatch_logger_init():
    """Pytest-compatible test for CloudWatchLogger initialization"""
    with patch("litellm.integrations.cloud_watch.litellm") as mock_litellm:
        mock_litellm.cloudwatch_callback_params = None
        mock_litellm.get_secret = lambda x: x.replace("os.environ/", "")
        
        with patch("litellm.integrations.cloud_watch.boto3") as mock_boto3:
            mock_client = MagicMock()
            mock_boto3.client.return_value = mock_client
            
            logger = CloudWatchLogger(
                log_group_name="test-group",
                log_stream_name="test-stream",
                aws_region="us-west-2",
            )
            
            assert logger.log_group_name == "test-group"
            assert logger.log_stream_name == "test-stream"
            mock_boto3.client.assert_called_once()


if __name__ == "__main__":
    unittest.main() 