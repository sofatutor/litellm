import asyncio
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import Request
from fastapi.responses import Response

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from litellm.proxy.utils import ProxyLogging, UserAPIKeyAuth
from litellm.caching.caching import DualCache


class TestAssistantsAPILogging(unittest.TestCase):
    """
    Tests for Assistants API logging functionality
    
    Tests the logging hooks for:
    - add_messages
    - get_assistants
    - run_thread
    """
    
    def setUp(self):
        """Set up test fixtures"""
        # Create mock request
        self.mock_request = MagicMock(spec=Request)
        self.mock_request.headers = {
            "x-litellm-call-id": "test-call-id",
            "content-type": "application/json",
        }
        
        # Create mock response
        self.mock_response = MagicMock(spec=Response)
        
        # Create a mock user_api_key_dict
        self.mock_user_api_key_dict = UserAPIKeyAuth(
            api_key="sk-test-key", 
            user_id="test-user",
        )
        
        # Create test data
        self.thread_id = "thread_abc123"
        self.test_data = {
            "model": "gpt-4-turbo",
            "messages": [{"role": "user", "content": "Hello, assistant"}],
        }

    async def _create_proxy_logging(self):
        """Create and configure a ProxyLogging instance for testing"""
        # Create a mock DualCache
        mock_cache = MagicMock(spec=DualCache)
        
        # Create a ProxyLogging instance with the mock cache
        proxy_logging = ProxyLogging(user_api_key_cache=mock_cache)
        
        # Mock the callbacks
        proxy_logging.pre_call_hooks = [AsyncMock()]
        
        return proxy_logging

    @pytest.mark.asyncio
    async def test_add_messages_logging(self):
        """Test that add_messages calls pre_call_hook with correct parameters"""
        # Arrange
        proxy_logging = await self._create_proxy_logging()
        
        # Act
        await proxy_logging.pre_call_hook(
            user_api_key_dict=self.mock_user_api_key_dict,
            data={
                "thread_id": self.thread_id,
                "role": "user",
                "content": "Hello, assistant",
                "litellm_call_id": "test-call-id",
            }, 
            call_type="add_messages",
        )
        
        # Assert
        proxy_logging.pre_call_hooks[0].assert_called_once()
        
        # Check the call arguments
        call_args = proxy_logging.pre_call_hooks[0].call_args[1]
        
        # Verify the call type was passed correctly
        assert call_args["call_type"] == "add_messages"
        
        # Verify the thread_id was passed
        assert call_args["data"]["thread_id"] == self.thread_id
    
    @pytest.mark.asyncio
    async def test_get_assistants_logging(self):
        """Test that get_assistants calls pre_call_hook with correct parameters"""
        # Arrange
        proxy_logging = await self._create_proxy_logging()
        
        # Act
        await proxy_logging.pre_call_hook(
            user_api_key_dict=self.mock_user_api_key_dict,
            data={
                "limit": 20,
                "order": "desc",
                "litellm_call_id": "test-call-id",
            }, 
            call_type="get_assistants",
        )
        
        # Assert
        proxy_logging.pre_call_hooks[0].assert_called_once()
        
        # Check the call arguments
        call_args = proxy_logging.pre_call_hooks[0].call_args[1]
        
        # Verify the call type was passed correctly
        assert call_args["call_type"] == "get_assistants"
        
        # Verify limit parameter exists
        assert call_args["data"]["limit"] == 20
    
    @pytest.mark.asyncio
    async def test_run_thread_logging(self):
        """Test that run_thread calls pre_call_hook with correct parameters"""
        # Arrange
        proxy_logging = await self._create_proxy_logging()
        
        # Test data specific to run_thread
        run_thread_data = {
            "thread_id": self.thread_id,
            "assistant_id": "asst_abc123",
            "instructions": "You are a helpful assistant.",
            "litellm_call_id": "test-call-id",
        }
        
        # Act
        await proxy_logging.pre_call_hook(
            user_api_key_dict=self.mock_user_api_key_dict,
            data=run_thread_data, 
            call_type="run_thread",
        )
        
        # Assert
        proxy_logging.pre_call_hooks[0].assert_called_once()
        
        # Check the call arguments
        call_args = proxy_logging.pre_call_hooks[0].call_args[1]
        
        # Verify the call type was passed correctly
        assert call_args["call_type"] == "run_thread"
        
        # Verify thread_id was passed
        assert call_args["data"]["thread_id"] == self.thread_id
        
        # Verify assistant_id was passed
        assert call_args["data"]["assistant_id"] == "asst_abc123"
    
    @pytest.mark.asyncio
    async def test_call_id_generation(self):
        """Test that a call_id is generated if not provided"""
        # Arrange
        proxy_logging = await self._create_proxy_logging()
        
        # Prepare data without call_id
        data_without_call_id = {
            "thread_id": self.thread_id,
            "role": "user",
            "content": "Hello, assistant",
        }
        
        # Act
        await proxy_logging.pre_call_hook(
            user_api_key_dict=self.mock_user_api_key_dict,
            data=data_without_call_id, 
            call_type="add_messages",
        )
        
        # Assert
        proxy_logging.pre_call_hooks[0].assert_called_once()
        
        # Check the call arguments
        call_args = proxy_logging.pre_call_hooks[0].call_args[1]
        
        # Verify a call_id was generated
        assert "litellm_call_id" in call_args["data"]
        assert call_args["data"]["litellm_call_id"] is not None
        assert isinstance(call_args["data"]["litellm_call_id"], str)


# For pytest compatibility
@pytest.mark.asyncio
async def test_proxy_logging_assistants_hooks():
    """Test that the ProxyLogging class has assistants API call types"""
    # Create a mock DualCache
    mock_cache = MagicMock(spec=DualCache)
    
    # Create a ProxyLogging instance with the mock cache
    proxy_logging = ProxyLogging(user_api_key_cache=mock_cache)
    
    # Create mock user API key dict
    mock_user_api_key_dict = UserAPIKeyAuth(
        api_key="sk-test-key", 
        user_id="test-user",
    )
    
    # Mock the callbacks
    proxy_logging.pre_call_hooks = [AsyncMock()]
    
    # Test data
    test_data = {
        "thread_id": "thread_abc123",
        "role": "user",
        "content": "Hello, assistant",
        "litellm_call_id": "test-call-id",
    }
    
    # Call the pre_call_hook with each assistants API call type
    for call_type in ["add_messages", "get_assistants", "run_thread"]:
        try:
            await proxy_logging.pre_call_hook(
                user_api_key_dict=mock_user_api_key_dict,
                data=test_data, 
                call_type=call_type,
            )
            # If we get here, the call type is supported
            assert True
        except Exception as e:
            # If we get an exception, the call type is not supported
            pytest.fail(f"Call type {call_type} is not supported: {str(e)}")


if __name__ == "__main__":
    unittest.main() 