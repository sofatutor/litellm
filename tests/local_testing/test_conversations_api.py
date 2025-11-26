"""
Unit tests for the Conversations API implementation.

These tests verify that the Conversations API endpoints and functions
are correctly implemented as part of the Responses API ecosystem.
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import litellm
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestConversationsAPIImports:
    """Test that all Conversations API components can be imported correctly."""

    def test_import_conversation_types(self):
        """Test importing conversation types from litellm.types.llms.openai."""
        from litellm.types.llms.openai import (
            Conversation,
            ConversationContentItem,
            ConversationCreateParams,
            ConversationDeletedResource,
            ConversationItem,
            ConversationItemCreateParams,
            ConversationItemList,
            ConversationItemListParams,
            ConversationUpdateParams,
        )

        # All imports should succeed
        assert Conversation is not None
        assert ConversationContentItem is not None
        assert ConversationCreateParams is not None
        assert ConversationDeletedResource is not None
        assert ConversationItem is not None
        assert ConversationItemCreateParams is not None
        assert ConversationItemList is not None
        assert ConversationItemListParams is not None
        assert ConversationUpdateParams is not None

    def test_import_conversation_functions(self):
        """Test importing conversation functions from litellm."""
        import litellm

        # Check that all expected functions are available
        assert hasattr(litellm, "acreate_conversation")
        assert hasattr(litellm, "create_conversation")
        assert hasattr(litellm, "aget_conversation")
        assert hasattr(litellm, "get_conversation")
        assert hasattr(litellm, "aupdate_conversation")
        assert hasattr(litellm, "update_conversation")
        assert hasattr(litellm, "adelete_conversation")
        assert hasattr(litellm, "delete_conversation")
        assert hasattr(litellm, "acreate_conversation_item")
        assert hasattr(litellm, "create_conversation_item")
        assert hasattr(litellm, "alist_conversation_items")
        assert hasattr(litellm, "list_conversation_items")
        assert hasattr(litellm, "aget_conversation_item")
        assert hasattr(litellm, "get_conversation_item")
        assert hasattr(litellm, "adelete_conversation_item")
        assert hasattr(litellm, "delete_conversation_item")

    def test_import_openai_conversations_api(self):
        """Test importing OpenAIConversationsAPI."""
        from litellm.llms.openai.conversations import OpenAIConversationsAPI

        api = OpenAIConversationsAPI()
        assert api is not None

        # Check that all expected methods are available
        assert hasattr(api, "create_conversation")
        assert hasattr(api, "acreate_conversation")
        assert hasattr(api, "get_conversation")
        assert hasattr(api, "aget_conversation")
        assert hasattr(api, "update_conversation")
        assert hasattr(api, "aupdate_conversation")
        assert hasattr(api, "delete_conversation")
        assert hasattr(api, "adelete_conversation")
        assert hasattr(api, "create_conversation_item")
        assert hasattr(api, "acreate_conversation_item")
        assert hasattr(api, "list_conversation_items")
        assert hasattr(api, "alist_conversation_items")
        assert hasattr(api, "get_conversation_item")
        assert hasattr(api, "aget_conversation_item")
        assert hasattr(api, "delete_conversation_item")
        assert hasattr(api, "adelete_conversation_item")

    def test_import_proxy_endpoints(self):
        """Test importing proxy conversation endpoints."""
        from litellm.proxy.conversation_endpoints.endpoints import router

        assert router is not None

        # Check that router has routes defined
        routes = [route.path for route in router.routes]
        assert "/v1/conversations" in routes or any("/conversations" in r for r in routes)


class TestConversationsAPIRouteMapping:
    """Test that route mappings are correctly defined."""

    def test_route_endpoint_mapping(self):
        """Test that conversation routes are in ROUTE_ENDPOINT_MAPPING."""
        from litellm.proxy.route_llm_request import ROUTE_ENDPOINT_MAPPING

        # Check conversation endpoint mappings
        assert "acreate_conversation" in ROUTE_ENDPOINT_MAPPING
        assert "aget_conversation" in ROUTE_ENDPOINT_MAPPING
        assert "aupdate_conversation" in ROUTE_ENDPOINT_MAPPING
        assert "adelete_conversation" in ROUTE_ENDPOINT_MAPPING
        assert "acreate_conversation_item" in ROUTE_ENDPOINT_MAPPING
        assert "alist_conversation_items" in ROUTE_ENDPOINT_MAPPING
        assert "aget_conversation_item" in ROUTE_ENDPOINT_MAPPING
        assert "adelete_conversation_item" in ROUTE_ENDPOINT_MAPPING

        # Check the mapped paths are correct
        assert ROUTE_ENDPOINT_MAPPING["acreate_conversation"] == "/conversations"
        assert (
            ROUTE_ENDPOINT_MAPPING["aget_conversation"]
            == "/conversations/{conversation_id}"
        )


class TestConversationsAPIRouter:
    """Test that router has conversation methods defined."""

    def test_router_conversation_methods(self):
        """Test that Router class has conversation methods."""
        from litellm.router import Router

        # Create a minimal router to check methods
        router = Router(
            model_list=[
                {
                    "model_name": "gpt-4",
                    "litellm_params": {
                        "model": "gpt-4",
                        "api_key": "test-key",
                    },
                }
            ]
        )

        # Check that all conversation methods are available
        assert hasattr(router, "acreate_conversation")
        assert hasattr(router, "aget_conversation")
        assert hasattr(router, "aupdate_conversation")
        assert hasattr(router, "adelete_conversation")
        assert hasattr(router, "acreate_conversation_item")
        assert hasattr(router, "alist_conversation_items")
        assert hasattr(router, "aget_conversation_item")
        assert hasattr(router, "adelete_conversation_item")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
