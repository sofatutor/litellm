"""
OpenAI Conversations API Implementation

This module provides the OpenAI-specific implementation of the Conversations API,
which is part of the Responses API ecosystem for managing stateful multi-turn conversations.
"""

import os
from typing import Any, Coroutine, Dict, List, Literal, Optional, Union

import httpx
from openai import AsyncOpenAI, OpenAI

import litellm
from litellm._logging import verbose_logger
from litellm.secret_managers.main import get_secret_str
from litellm.types.llms.openai import (
    Conversation,
    ConversationContentItem,
    ConversationDeletedResource,
    ConversationItem,
    ConversationItemList,
)


class OpenAIConversationsAPI:
    """
    OpenAI Conversations API implementation.

    This class provides methods for creating, retrieving, updating, and deleting
    conversations and conversation items via the OpenAI API.
    """

    def __init__(self):
        pass

    def _get_openai_client(
        self,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        max_retries: int = 2,
        organization: Optional[str] = None,
        **kwargs,
    ) -> OpenAI:
        """Get a synchronous OpenAI client."""
        # Get API key from params, env, or secret manager
        if api_key is None:
            api_key = (
                litellm.api_key
                or get_secret_str("OPENAI_API_KEY")
                or os.getenv("OPENAI_API_KEY")
            )

        # Get base URL
        if api_base is None:
            api_base = (
                litellm.api_base
                or get_secret_str("OPENAI_API_BASE")
                or os.getenv("OPENAI_API_BASE")
                or "https://api.openai.com/v1"
            )

        # Get organization
        if organization is None:
            organization = (
                litellm.organization
                or get_secret_str("OPENAI_ORGANIZATION")
                or os.getenv("OPENAI_ORGANIZATION")
            )

        client = OpenAI(
            api_key=api_key,
            base_url=api_base,
            timeout=timeout,
            max_retries=max_retries,
            organization=organization,
        )

        return client

    def _get_async_openai_client(
        self,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        max_retries: int = 2,
        organization: Optional[str] = None,
        **kwargs,
    ) -> AsyncOpenAI:
        """Get an asynchronous OpenAI client."""
        # Get API key from params, env, or secret manager
        if api_key is None:
            api_key = (
                litellm.api_key
                or get_secret_str("OPENAI_API_KEY")
                or os.getenv("OPENAI_API_KEY")
            )

        # Get base URL
        if api_base is None:
            api_base = (
                litellm.api_base
                or get_secret_str("OPENAI_API_BASE")
                or os.getenv("OPENAI_API_BASE")
                or "https://api.openai.com/v1"
            )

        # Get organization
        if organization is None:
            organization = (
                litellm.organization
                or get_secret_str("OPENAI_ORGANIZATION")
                or os.getenv("OPENAI_ORGANIZATION")
            )

        client = AsyncOpenAI(
            api_key=api_key,
            base_url=api_base,
            timeout=timeout,
            max_retries=max_retries,
            organization=organization,
        )

        return client

    def _response_to_dict(self, response: Any) -> Dict[str, Any]:
        """Convert an OpenAI response object to a dictionary."""
        if hasattr(response, "model_dump"):
            return response.model_dump()
        elif hasattr(response, "to_dict"):
            return response.to_dict()
        elif hasattr(response, "__dict__"):
            return dict(response.__dict__)
        else:
            return dict(response)

    ####### CONVERSATION CRUD OPERATIONS ###################

    def create_conversation(
        self,
        metadata: Optional[Dict[str, str]] = None,
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        **kwargs,
    ) -> Conversation:
        """
        Create a new conversation.

        Args:
            metadata: Optional metadata to attach to the conversation.
            extra_headers: Additional headers to send with the request.
            extra_query: Additional query parameters.
            extra_body: Additional body parameters.
            timeout: Request timeout.
            api_key: OpenAI API key.
            api_base: OpenAI API base URL.

        Returns:
            Conversation: The created conversation object.
        """
        client = self._get_openai_client(
            api_key=api_key,
            api_base=api_base,
            timeout=timeout,
        )

        # Build request parameters
        request_params: Dict[str, Any] = {}
        if metadata is not None:
            request_params["metadata"] = metadata
        if extra_headers is not None:
            request_params["extra_headers"] = extra_headers
        if extra_query is not None:
            request_params["extra_query"] = extra_query
        if extra_body is not None:
            request_params["extra_body"] = extra_body
        if timeout is not None:
            request_params["timeout"] = timeout

        verbose_logger.debug(f"Creating conversation with params: {request_params}")

        response = client.conversations.create(**request_params)

        return self._response_to_dict(response)  # type: ignore

    async def acreate_conversation(
        self,
        metadata: Optional[Dict[str, str]] = None,
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        **kwargs,
    ) -> Coroutine[Any, Any, Conversation]:
        """
        Async: Create a new conversation.

        Args:
            metadata: Optional metadata to attach to the conversation.
            extra_headers: Additional headers to send with the request.
            extra_query: Additional query parameters.
            extra_body: Additional body parameters.
            timeout: Request timeout.
            api_key: OpenAI API key.
            api_base: OpenAI API base URL.

        Returns:
            Conversation: The created conversation object.
        """
        client = self._get_async_openai_client(
            api_key=api_key,
            api_base=api_base,
            timeout=timeout,
        )

        # Build request parameters
        request_params: Dict[str, Any] = {}
        if metadata is not None:
            request_params["metadata"] = metadata
        if extra_headers is not None:
            request_params["extra_headers"] = extra_headers
        if extra_query is not None:
            request_params["extra_query"] = extra_query
        if extra_body is not None:
            request_params["extra_body"] = extra_body
        if timeout is not None:
            request_params["timeout"] = timeout

        verbose_logger.debug(f"Creating conversation with params: {request_params}")

        response = await client.conversations.create(**request_params)

        return self._response_to_dict(response)  # type: ignore

    def get_conversation(
        self,
        conversation_id: str,
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        **kwargs,
    ) -> Conversation:
        """
        Retrieve a conversation by ID.

        Args:
            conversation_id: The ID of the conversation to retrieve.
            extra_headers: Additional headers to send with the request.
            extra_query: Additional query parameters.
            extra_body: Additional body parameters.
            timeout: Request timeout.
            api_key: OpenAI API key.
            api_base: OpenAI API base URL.

        Returns:
            Conversation: The retrieved conversation object.
        """
        client = self._get_openai_client(
            api_key=api_key,
            api_base=api_base,
            timeout=timeout,
        )

        # Build request parameters
        request_params: Dict[str, Any] = {}
        if extra_headers is not None:
            request_params["extra_headers"] = extra_headers
        if extra_query is not None:
            request_params["extra_query"] = extra_query
        if extra_body is not None:
            request_params["extra_body"] = extra_body
        if timeout is not None:
            request_params["timeout"] = timeout

        verbose_logger.debug(
            f"Retrieving conversation {conversation_id} with params: {request_params}"
        )

        response = client.conversations.retrieve(conversation_id, **request_params)

        return self._response_to_dict(response)  # type: ignore

    async def aget_conversation(
        self,
        conversation_id: str,
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        **kwargs,
    ) -> Coroutine[Any, Any, Conversation]:
        """
        Async: Retrieve a conversation by ID.

        Args:
            conversation_id: The ID of the conversation to retrieve.
            extra_headers: Additional headers to send with the request.
            extra_query: Additional query parameters.
            extra_body: Additional body parameters.
            timeout: Request timeout.
            api_key: OpenAI API key.
            api_base: OpenAI API base URL.

        Returns:
            Conversation: The retrieved conversation object.
        """
        client = self._get_async_openai_client(
            api_key=api_key,
            api_base=api_base,
            timeout=timeout,
        )

        # Build request parameters
        request_params: Dict[str, Any] = {}
        if extra_headers is not None:
            request_params["extra_headers"] = extra_headers
        if extra_query is not None:
            request_params["extra_query"] = extra_query
        if extra_body is not None:
            request_params["extra_body"] = extra_body
        if timeout is not None:
            request_params["timeout"] = timeout

        verbose_logger.debug(
            f"Retrieving conversation {conversation_id} with params: {request_params}"
        )

        response = await client.conversations.retrieve(conversation_id, **request_params)

        return self._response_to_dict(response)  # type: ignore

    def update_conversation(
        self,
        conversation_id: str,
        metadata: Optional[Dict[str, str]] = None,
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        **kwargs,
    ) -> Conversation:
        """
        Update a conversation.

        Args:
            conversation_id: The ID of the conversation to update.
            metadata: New metadata to set on the conversation.
            extra_headers: Additional headers to send with the request.
            extra_query: Additional query parameters.
            extra_body: Additional body parameters.
            timeout: Request timeout.
            api_key: OpenAI API key.
            api_base: OpenAI API base URL.

        Returns:
            Conversation: The updated conversation object.
        """
        client = self._get_openai_client(
            api_key=api_key,
            api_base=api_base,
            timeout=timeout,
        )

        # Build request parameters
        request_params: Dict[str, Any] = {}
        if metadata is not None:
            request_params["metadata"] = metadata
        if extra_headers is not None:
            request_params["extra_headers"] = extra_headers
        if extra_query is not None:
            request_params["extra_query"] = extra_query
        if extra_body is not None:
            request_params["extra_body"] = extra_body
        if timeout is not None:
            request_params["timeout"] = timeout

        verbose_logger.debug(
            f"Updating conversation {conversation_id} with params: {request_params}"
        )

        response = client.conversations.update(conversation_id, **request_params)

        return self._response_to_dict(response)  # type: ignore

    async def aupdate_conversation(
        self,
        conversation_id: str,
        metadata: Optional[Dict[str, str]] = None,
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        **kwargs,
    ) -> Coroutine[Any, Any, Conversation]:
        """
        Async: Update a conversation.

        Args:
            conversation_id: The ID of the conversation to update.
            metadata: New metadata to set on the conversation.
            extra_headers: Additional headers to send with the request.
            extra_query: Additional query parameters.
            extra_body: Additional body parameters.
            timeout: Request timeout.
            api_key: OpenAI API key.
            api_base: OpenAI API base URL.

        Returns:
            Conversation: The updated conversation object.
        """
        client = self._get_async_openai_client(
            api_key=api_key,
            api_base=api_base,
            timeout=timeout,
        )

        # Build request parameters
        request_params: Dict[str, Any] = {}
        if metadata is not None:
            request_params["metadata"] = metadata
        if extra_headers is not None:
            request_params["extra_headers"] = extra_headers
        if extra_query is not None:
            request_params["extra_query"] = extra_query
        if extra_body is not None:
            request_params["extra_body"] = extra_body
        if timeout is not None:
            request_params["timeout"] = timeout

        verbose_logger.debug(
            f"Updating conversation {conversation_id} with params: {request_params}"
        )

        response = await client.conversations.update(conversation_id, **request_params)

        return self._response_to_dict(response)  # type: ignore

    def delete_conversation(
        self,
        conversation_id: str,
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        **kwargs,
    ) -> ConversationDeletedResource:
        """
        Delete a conversation.

        Args:
            conversation_id: The ID of the conversation to delete.
            extra_headers: Additional headers to send with the request.
            extra_query: Additional query parameters.
            extra_body: Additional body parameters.
            timeout: Request timeout.
            api_key: OpenAI API key.
            api_base: OpenAI API base URL.

        Returns:
            ConversationDeletedResource: Confirmation of deletion.
        """
        client = self._get_openai_client(
            api_key=api_key,
            api_base=api_base,
            timeout=timeout,
        )

        # Build request parameters
        request_params: Dict[str, Any] = {}
        if extra_headers is not None:
            request_params["extra_headers"] = extra_headers
        if extra_query is not None:
            request_params["extra_query"] = extra_query
        if extra_body is not None:
            request_params["extra_body"] = extra_body
        if timeout is not None:
            request_params["timeout"] = timeout

        verbose_logger.debug(
            f"Deleting conversation {conversation_id} with params: {request_params}"
        )

        response = client.conversations.delete(conversation_id, **request_params)

        return self._response_to_dict(response)  # type: ignore

    async def adelete_conversation(
        self,
        conversation_id: str,
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        **kwargs,
    ) -> Coroutine[Any, Any, ConversationDeletedResource]:
        """
        Async: Delete a conversation.

        Args:
            conversation_id: The ID of the conversation to delete.
            extra_headers: Additional headers to send with the request.
            extra_query: Additional query parameters.
            extra_body: Additional body parameters.
            timeout: Request timeout.
            api_key: OpenAI API key.
            api_base: OpenAI API base URL.

        Returns:
            ConversationDeletedResource: Confirmation of deletion.
        """
        client = self._get_async_openai_client(
            api_key=api_key,
            api_base=api_base,
            timeout=timeout,
        )

        # Build request parameters
        request_params: Dict[str, Any] = {}
        if extra_headers is not None:
            request_params["extra_headers"] = extra_headers
        if extra_query is not None:
            request_params["extra_query"] = extra_query
        if extra_body is not None:
            request_params["extra_body"] = extra_body
        if timeout is not None:
            request_params["timeout"] = timeout

        verbose_logger.debug(
            f"Deleting conversation {conversation_id} with params: {request_params}"
        )

        response = await client.conversations.delete(conversation_id, **request_params)

        return self._response_to_dict(response)  # type: ignore

    ####### CONVERSATION ITEM CRUD OPERATIONS ###################

    def create_conversation_item(
        self,
        conversation_id: str,
        type: str,
        role: Optional[str] = None,
        content: Optional[List[ConversationContentItem]] = None,
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        **kwargs,
    ) -> ConversationItem:
        """
        Create a new item in a conversation.

        Args:
            conversation_id: The ID of the conversation to add the item to.
            type: The type of item (e.g., "message", "function_call").
            role: The role of the item creator (e.g., "user", "assistant").
            content: The content of the item.
            extra_headers: Additional headers to send with the request.
            extra_query: Additional query parameters.
            extra_body: Additional body parameters.
            timeout: Request timeout.
            api_key: OpenAI API key.
            api_base: OpenAI API base URL.

        Returns:
            ConversationItem: The created conversation item.
        """
        client = self._get_openai_client(
            api_key=api_key,
            api_base=api_base,
            timeout=timeout,
        )

        # Build request parameters
        request_params: Dict[str, Any] = {"type": type}
        if role is not None:
            request_params["role"] = role
        if content is not None:
            request_params["content"] = content
        if extra_headers is not None:
            request_params["extra_headers"] = extra_headers
        if extra_query is not None:
            request_params["extra_query"] = extra_query
        if extra_body is not None:
            request_params["extra_body"] = extra_body
        if timeout is not None:
            request_params["timeout"] = timeout

        verbose_logger.debug(
            f"Creating item in conversation {conversation_id} with params: {request_params}"
        )

        response = client.conversations.items.create(conversation_id, **request_params)

        return self._response_to_dict(response)  # type: ignore

    async def acreate_conversation_item(
        self,
        conversation_id: str,
        type: str,
        role: Optional[str] = None,
        content: Optional[List[ConversationContentItem]] = None,
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        **kwargs,
    ) -> Coroutine[Any, Any, ConversationItem]:
        """
        Async: Create a new item in a conversation.

        Args:
            conversation_id: The ID of the conversation to add the item to.
            type: The type of item (e.g., "message", "function_call").
            role: The role of the item creator (e.g., "user", "assistant").
            content: The content of the item.
            extra_headers: Additional headers to send with the request.
            extra_query: Additional query parameters.
            extra_body: Additional body parameters.
            timeout: Request timeout.
            api_key: OpenAI API key.
            api_base: OpenAI API base URL.

        Returns:
            ConversationItem: The created conversation item.
        """
        client = self._get_async_openai_client(
            api_key=api_key,
            api_base=api_base,
            timeout=timeout,
        )

        # Build request parameters
        request_params: Dict[str, Any] = {"type": type}
        if role is not None:
            request_params["role"] = role
        if content is not None:
            request_params["content"] = content
        if extra_headers is not None:
            request_params["extra_headers"] = extra_headers
        if extra_query is not None:
            request_params["extra_query"] = extra_query
        if extra_body is not None:
            request_params["extra_body"] = extra_body
        if timeout is not None:
            request_params["timeout"] = timeout

        verbose_logger.debug(
            f"Creating item in conversation {conversation_id} with params: {request_params}"
        )

        response = await client.conversations.items.create(
            conversation_id, **request_params
        )

        return self._response_to_dict(response)  # type: ignore

    def list_conversation_items(
        self,
        conversation_id: str,
        limit: Optional[int] = None,
        order: Optional[Literal["asc", "desc"]] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        **kwargs,
    ) -> ConversationItemList:
        """
        List items in a conversation.

        Args:
            conversation_id: The ID of the conversation.
            limit: Maximum number of items to return.
            order: Sort order ("asc" or "desc").
            after: Return items after this ID (for pagination).
            before: Return items before this ID (for pagination).
            extra_headers: Additional headers to send with the request.
            extra_query: Additional query parameters.
            extra_body: Additional body parameters.
            timeout: Request timeout.
            api_key: OpenAI API key.
            api_base: OpenAI API base URL.

        Returns:
            ConversationItemList: List of conversation items.
        """
        client = self._get_openai_client(
            api_key=api_key,
            api_base=api_base,
            timeout=timeout,
        )

        # Build request parameters
        request_params: Dict[str, Any] = {}
        if limit is not None:
            request_params["limit"] = limit
        if order is not None:
            request_params["order"] = order
        if after is not None:
            request_params["after"] = after
        if before is not None:
            request_params["before"] = before
        if extra_headers is not None:
            request_params["extra_headers"] = extra_headers
        if extra_query is not None:
            request_params["extra_query"] = extra_query
        if extra_body is not None:
            request_params["extra_body"] = extra_body
        if timeout is not None:
            request_params["timeout"] = timeout

        verbose_logger.debug(
            f"Listing items in conversation {conversation_id} with params: {request_params}"
        )

        response = client.conversations.items.list(conversation_id, **request_params)

        # Handle SyncCursorPage response
        items_data = []
        for item in response:
            items_data.append(self._response_to_dict(item))

        return {
            "object": "list",
            "data": items_data,
            "first_id": items_data[0]["id"] if items_data else None,
            "last_id": items_data[-1]["id"] if items_data else None,
            "has_more": response.has_more if hasattr(response, "has_more") else False,
        }  # type: ignore

    async def alist_conversation_items(
        self,
        conversation_id: str,
        limit: Optional[int] = None,
        order: Optional[Literal["asc", "desc"]] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        **kwargs,
    ) -> Coroutine[Any, Any, ConversationItemList]:
        """
        Async: List items in a conversation.

        Args:
            conversation_id: The ID of the conversation.
            limit: Maximum number of items to return.
            order: Sort order ("asc" or "desc").
            after: Return items after this ID (for pagination).
            before: Return items before this ID (for pagination).
            extra_headers: Additional headers to send with the request.
            extra_query: Additional query parameters.
            extra_body: Additional body parameters.
            timeout: Request timeout.
            api_key: OpenAI API key.
            api_base: OpenAI API base URL.

        Returns:
            ConversationItemList: List of conversation items.
        """
        client = self._get_async_openai_client(
            api_key=api_key,
            api_base=api_base,
            timeout=timeout,
        )

        # Build request parameters
        request_params: Dict[str, Any] = {}
        if limit is not None:
            request_params["limit"] = limit
        if order is not None:
            request_params["order"] = order
        if after is not None:
            request_params["after"] = after
        if before is not None:
            request_params["before"] = before
        if extra_headers is not None:
            request_params["extra_headers"] = extra_headers
        if extra_query is not None:
            request_params["extra_query"] = extra_query
        if extra_body is not None:
            request_params["extra_body"] = extra_body
        if timeout is not None:
            request_params["timeout"] = timeout

        verbose_logger.debug(
            f"Listing items in conversation {conversation_id} with params: {request_params}"
        )

        response = await client.conversations.items.list(
            conversation_id, **request_params
        )

        # Handle AsyncCursorPage response
        items_data = []
        async for item in response:
            items_data.append(self._response_to_dict(item))

        return {
            "object": "list",
            "data": items_data,
            "first_id": items_data[0]["id"] if items_data else None,
            "last_id": items_data[-1]["id"] if items_data else None,
            "has_more": response.has_more if hasattr(response, "has_more") else False,
        }  # type: ignore

    def get_conversation_item(
        self,
        conversation_id: str,
        item_id: str,
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        **kwargs,
    ) -> ConversationItem:
        """
        Retrieve a specific item from a conversation.

        Args:
            conversation_id: The ID of the conversation.
            item_id: The ID of the item to retrieve.
            extra_headers: Additional headers to send with the request.
            extra_query: Additional query parameters.
            extra_body: Additional body parameters.
            timeout: Request timeout.
            api_key: OpenAI API key.
            api_base: OpenAI API base URL.

        Returns:
            ConversationItem: The retrieved conversation item.
        """
        client = self._get_openai_client(
            api_key=api_key,
            api_base=api_base,
            timeout=timeout,
        )

        # Build request parameters
        request_params: Dict[str, Any] = {}
        if extra_headers is not None:
            request_params["extra_headers"] = extra_headers
        if extra_query is not None:
            request_params["extra_query"] = extra_query
        if extra_body is not None:
            request_params["extra_body"] = extra_body
        if timeout is not None:
            request_params["timeout"] = timeout

        verbose_logger.debug(
            f"Retrieving item {item_id} from conversation {conversation_id} with params: {request_params}"
        )

        response = client.conversations.items.retrieve(
            conversation_id, item_id, **request_params
        )

        return self._response_to_dict(response)  # type: ignore

    async def aget_conversation_item(
        self,
        conversation_id: str,
        item_id: str,
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        **kwargs,
    ) -> Coroutine[Any, Any, ConversationItem]:
        """
        Async: Retrieve a specific item from a conversation.

        Args:
            conversation_id: The ID of the conversation.
            item_id: The ID of the item to retrieve.
            extra_headers: Additional headers to send with the request.
            extra_query: Additional query parameters.
            extra_body: Additional body parameters.
            timeout: Request timeout.
            api_key: OpenAI API key.
            api_base: OpenAI API base URL.

        Returns:
            ConversationItem: The retrieved conversation item.
        """
        client = self._get_async_openai_client(
            api_key=api_key,
            api_base=api_base,
            timeout=timeout,
        )

        # Build request parameters
        request_params: Dict[str, Any] = {}
        if extra_headers is not None:
            request_params["extra_headers"] = extra_headers
        if extra_query is not None:
            request_params["extra_query"] = extra_query
        if extra_body is not None:
            request_params["extra_body"] = extra_body
        if timeout is not None:
            request_params["timeout"] = timeout

        verbose_logger.debug(
            f"Retrieving item {item_id} from conversation {conversation_id} with params: {request_params}"
        )

        response = await client.conversations.items.retrieve(
            conversation_id, item_id, **request_params
        )

        return self._response_to_dict(response)  # type: ignore

    def delete_conversation_item(
        self,
        conversation_id: str,
        item_id: str,
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        **kwargs,
    ) -> ConversationDeletedResource:
        """
        Delete a specific item from a conversation.

        Args:
            conversation_id: The ID of the conversation.
            item_id: The ID of the item to delete.
            extra_headers: Additional headers to send with the request.
            extra_query: Additional query parameters.
            extra_body: Additional body parameters.
            timeout: Request timeout.
            api_key: OpenAI API key.
            api_base: OpenAI API base URL.

        Returns:
            ConversationDeletedResource: Confirmation of deletion.
        """
        client = self._get_openai_client(
            api_key=api_key,
            api_base=api_base,
            timeout=timeout,
        )

        # Build request parameters
        request_params: Dict[str, Any] = {}
        if extra_headers is not None:
            request_params["extra_headers"] = extra_headers
        if extra_query is not None:
            request_params["extra_query"] = extra_query
        if extra_body is not None:
            request_params["extra_body"] = extra_body
        if timeout is not None:
            request_params["timeout"] = timeout

        verbose_logger.debug(
            f"Deleting item {item_id} from conversation {conversation_id} with params: {request_params}"
        )

        response = client.conversations.items.delete(
            conversation_id, item_id, **request_params
        )

        return self._response_to_dict(response)  # type: ignore

    async def adelete_conversation_item(
        self,
        conversation_id: str,
        item_id: str,
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        **kwargs,
    ) -> Coroutine[Any, Any, ConversationDeletedResource]:
        """
        Async: Delete a specific item from a conversation.

        Args:
            conversation_id: The ID of the conversation.
            item_id: The ID of the item to delete.
            extra_headers: Additional headers to send with the request.
            extra_query: Additional query parameters.
            extra_body: Additional body parameters.
            timeout: Request timeout.
            api_key: OpenAI API key.
            api_base: OpenAI API base URL.

        Returns:
            ConversationDeletedResource: Confirmation of deletion.
        """
        client = self._get_async_openai_client(
            api_key=api_key,
            api_base=api_base,
            timeout=timeout,
        )

        # Build request parameters
        request_params: Dict[str, Any] = {}
        if extra_headers is not None:
            request_params["extra_headers"] = extra_headers
        if extra_query is not None:
            request_params["extra_query"] = extra_query
        if extra_body is not None:
            request_params["extra_body"] = extra_body
        if timeout is not None:
            request_params["timeout"] = timeout

        verbose_logger.debug(
            f"Deleting item {item_id} from conversation {conversation_id} with params: {request_params}"
        )

        response = await client.conversations.items.delete(
            conversation_id, item_id, **request_params
        )

        return self._response_to_dict(response)  # type: ignore
