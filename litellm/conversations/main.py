"""
LiteLLM Conversations API

This module provides the Conversations API implementation, which is part of the
OpenAI Responses API ecosystem for managing stateful multi-turn conversations.

The Conversations API provides:
- Create, retrieve, update, and delete conversations
- Manage conversation items (messages, function calls, etc.)
- Stateful conversation management for the Responses API

Usage:
    import litellm

    # Create a conversation
    conversation = await litellm.acreate_conversation()

    # Add items to conversation
    item = await litellm.acreate_conversation_item(
        conversation_id=conversation.id,
        type="message",
        role="user",
        content=[{"type": "input_text", "text": "Hello!"}]
    )

    # Use conversation with Responses API
    response = await litellm.aresponses(
        model="gpt-4o",
        input="Continue the conversation",
        conversation_id=conversation.id
    )
"""

import asyncio
import contextvars
from functools import partial
from typing import Any, Dict, List, Literal, Optional, Union

import httpx

import litellm
from litellm._logging import verbose_logger
from litellm.constants import request_timeout
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
from litellm.utils import client

# Type aliases for clarity
ConversationId = str
ItemId = str


####### CONVERSATION CRUD OPERATIONS ###################


@client
async def acreate_conversation(
    metadata: Optional[Dict[str, str]] = None,
    # Use the following arguments if you need to pass additional parameters to the API
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs,
) -> Conversation:
    """
    Async: Create a new conversation.

    Args:
        metadata: Optional metadata to attach to the conversation.
        extra_headers: Additional headers to send with the request.
        extra_query: Additional query parameters to send with the request.
        extra_body: Additional body parameters to send with the request.
        timeout: Request timeout.
        custom_llm_provider: The LLM provider to use (defaults to "openai").
        api_key: API key for the provider.
        api_base: Base URL for the API.
        **kwargs: Additional arguments.

    Returns:
        Conversation: The created conversation object.
    """
    local_vars = locals()
    try:
        loop = asyncio.get_event_loop()
        kwargs["acreate_conversation"] = True

        func = partial(
            create_conversation,
            metadata=metadata,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            custom_llm_provider=custom_llm_provider,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )

        ctx = contextvars.copy_context()
        func_with_context = partial(ctx.run, func)
        init_response = await loop.run_in_executor(None, func_with_context)

        if asyncio.iscoroutine(init_response):
            response = await init_response
        else:
            response = init_response

        return response
    except Exception as e:
        raise litellm.exception_type(
            model="",
            custom_llm_provider=custom_llm_provider or "openai",
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


@client
def create_conversation(
    metadata: Optional[Dict[str, str]] = None,
    # Use the following arguments if you need to pass additional parameters to the API
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs,
) -> Conversation:
    """
    Sync: Create a new conversation.

    Args:
        metadata: Optional metadata to attach to the conversation.
        extra_headers: Additional headers to send with the request.
        extra_query: Additional query parameters to send with the request.
        extra_body: Additional body parameters to send with the request.
        timeout: Request timeout.
        custom_llm_provider: The LLM provider to use (defaults to "openai").
        api_key: API key for the provider.
        api_base: Base URL for the API.
        **kwargs: Additional arguments.

    Returns:
        Conversation: The created conversation object.
    """
    from litellm.llms.openai.conversations import OpenAIConversationsAPI

    _is_async = kwargs.pop("acreate_conversation", False) is True

    # Default to OpenAI if no provider specified
    if custom_llm_provider is None:
        custom_llm_provider = "openai"

    openai_conversations_api = OpenAIConversationsAPI()

    if _is_async:
        return openai_conversations_api.acreate_conversation(
            metadata=metadata,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )
    else:
        return openai_conversations_api.create_conversation(
            metadata=metadata,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )


@client
async def aget_conversation(
    conversation_id: str,
    # Use the following arguments if you need to pass additional parameters to the API
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs,
) -> Conversation:
    """
    Async: Retrieve a conversation by ID.

    Args:
        conversation_id: The ID of the conversation to retrieve.
        extra_headers: Additional headers to send with the request.
        extra_query: Additional query parameters to send with the request.
        extra_body: Additional body parameters to send with the request.
        timeout: Request timeout.
        custom_llm_provider: The LLM provider to use (defaults to "openai").
        api_key: API key for the provider.
        api_base: Base URL for the API.
        **kwargs: Additional arguments.

    Returns:
        Conversation: The retrieved conversation object.
    """
    local_vars = locals()
    try:
        loop = asyncio.get_event_loop()
        kwargs["aget_conversation"] = True

        func = partial(
            get_conversation,
            conversation_id=conversation_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            custom_llm_provider=custom_llm_provider,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )

        ctx = contextvars.copy_context()
        func_with_context = partial(ctx.run, func)
        init_response = await loop.run_in_executor(None, func_with_context)

        if asyncio.iscoroutine(init_response):
            response = await init_response
        else:
            response = init_response

        return response
    except Exception as e:
        raise litellm.exception_type(
            model="",
            custom_llm_provider=custom_llm_provider or "openai",
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


@client
def get_conversation(
    conversation_id: str,
    # Use the following arguments if you need to pass additional parameters to the API
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs,
) -> Conversation:
    """
    Sync: Retrieve a conversation by ID.

    Args:
        conversation_id: The ID of the conversation to retrieve.
        extra_headers: Additional headers to send with the request.
        extra_query: Additional query parameters to send with the request.
        extra_body: Additional body parameters to send with the request.
        timeout: Request timeout.
        custom_llm_provider: The LLM provider to use (defaults to "openai").
        api_key: API key for the provider.
        api_base: Base URL for the API.
        **kwargs: Additional arguments.

    Returns:
        Conversation: The retrieved conversation object.
    """
    from litellm.llms.openai.conversations import OpenAIConversationsAPI

    _is_async = kwargs.pop("aget_conversation", False) is True

    # Default to OpenAI if no provider specified
    if custom_llm_provider is None:
        custom_llm_provider = "openai"

    openai_conversations_api = OpenAIConversationsAPI()

    if _is_async:
        return openai_conversations_api.aget_conversation(
            conversation_id=conversation_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )
    else:
        return openai_conversations_api.get_conversation(
            conversation_id=conversation_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )


@client
async def aupdate_conversation(
    conversation_id: str,
    metadata: Optional[Dict[str, str]] = None,
    # Use the following arguments if you need to pass additional parameters to the API
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs,
) -> Conversation:
    """
    Async: Update a conversation.

    Args:
        conversation_id: The ID of the conversation to update.
        metadata: New metadata to set on the conversation.
        extra_headers: Additional headers to send with the request.
        extra_query: Additional query parameters to send with the request.
        extra_body: Additional body parameters to send with the request.
        timeout: Request timeout.
        custom_llm_provider: The LLM provider to use (defaults to "openai").
        api_key: API key for the provider.
        api_base: Base URL for the API.
        **kwargs: Additional arguments.

    Returns:
        Conversation: The updated conversation object.
    """
    local_vars = locals()
    try:
        loop = asyncio.get_event_loop()
        kwargs["aupdate_conversation"] = True

        func = partial(
            update_conversation,
            conversation_id=conversation_id,
            metadata=metadata,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            custom_llm_provider=custom_llm_provider,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )

        ctx = contextvars.copy_context()
        func_with_context = partial(ctx.run, func)
        init_response = await loop.run_in_executor(None, func_with_context)

        if asyncio.iscoroutine(init_response):
            response = await init_response
        else:
            response = init_response

        return response
    except Exception as e:
        raise litellm.exception_type(
            model="",
            custom_llm_provider=custom_llm_provider or "openai",
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


@client
def update_conversation(
    conversation_id: str,
    metadata: Optional[Dict[str, str]] = None,
    # Use the following arguments if you need to pass additional parameters to the API
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs,
) -> Conversation:
    """
    Sync: Update a conversation.

    Args:
        conversation_id: The ID of the conversation to update.
        metadata: New metadata to set on the conversation.
        extra_headers: Additional headers to send with the request.
        extra_query: Additional query parameters to send with the request.
        extra_body: Additional body parameters to send with the request.
        timeout: Request timeout.
        custom_llm_provider: The LLM provider to use (defaults to "openai").
        api_key: API key for the provider.
        api_base: Base URL for the API.
        **kwargs: Additional arguments.

    Returns:
        Conversation: The updated conversation object.
    """
    from litellm.llms.openai.conversations import OpenAIConversationsAPI

    _is_async = kwargs.pop("aupdate_conversation", False) is True

    # Default to OpenAI if no provider specified
    if custom_llm_provider is None:
        custom_llm_provider = "openai"

    openai_conversations_api = OpenAIConversationsAPI()

    if _is_async:
        return openai_conversations_api.aupdate_conversation(
            conversation_id=conversation_id,
            metadata=metadata,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )
    else:
        return openai_conversations_api.update_conversation(
            conversation_id=conversation_id,
            metadata=metadata,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )


@client
async def adelete_conversation(
    conversation_id: str,
    # Use the following arguments if you need to pass additional parameters to the API
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs,
) -> ConversationDeletedResource:
    """
    Async: Delete a conversation.

    Args:
        conversation_id: The ID of the conversation to delete.
        extra_headers: Additional headers to send with the request.
        extra_query: Additional query parameters to send with the request.
        extra_body: Additional body parameters to send with the request.
        timeout: Request timeout.
        custom_llm_provider: The LLM provider to use (defaults to "openai").
        api_key: API key for the provider.
        api_base: Base URL for the API.
        **kwargs: Additional arguments.

    Returns:
        ConversationDeletedResource: Confirmation of deletion.
    """
    local_vars = locals()
    try:
        loop = asyncio.get_event_loop()
        kwargs["adelete_conversation"] = True

        func = partial(
            delete_conversation,
            conversation_id=conversation_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            custom_llm_provider=custom_llm_provider,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )

        ctx = contextvars.copy_context()
        func_with_context = partial(ctx.run, func)
        init_response = await loop.run_in_executor(None, func_with_context)

        if asyncio.iscoroutine(init_response):
            response = await init_response
        else:
            response = init_response

        return response
    except Exception as e:
        raise litellm.exception_type(
            model="",
            custom_llm_provider=custom_llm_provider or "openai",
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


@client
def delete_conversation(
    conversation_id: str,
    # Use the following arguments if you need to pass additional parameters to the API
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs,
) -> ConversationDeletedResource:
    """
    Sync: Delete a conversation.

    Args:
        conversation_id: The ID of the conversation to delete.
        extra_headers: Additional headers to send with the request.
        extra_query: Additional query parameters to send with the request.
        extra_body: Additional body parameters to send with the request.
        timeout: Request timeout.
        custom_llm_provider: The LLM provider to use (defaults to "openai").
        api_key: API key for the provider.
        api_base: Base URL for the API.
        **kwargs: Additional arguments.

    Returns:
        ConversationDeletedResource: Confirmation of deletion.
    """
    from litellm.llms.openai.conversations import OpenAIConversationsAPI

    _is_async = kwargs.pop("adelete_conversation", False) is True

    # Default to OpenAI if no provider specified
    if custom_llm_provider is None:
        custom_llm_provider = "openai"

    openai_conversations_api = OpenAIConversationsAPI()

    if _is_async:
        return openai_conversations_api.adelete_conversation(
            conversation_id=conversation_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )
    else:
        return openai_conversations_api.delete_conversation(
            conversation_id=conversation_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )


####### CONVERSATION ITEM CRUD OPERATIONS ###################


@client
async def acreate_conversation_item(
    conversation_id: str,
    type: str,
    role: Optional[str] = None,
    content: Optional[List[ConversationContentItem]] = None,
    # Use the following arguments if you need to pass additional parameters to the API
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs,
) -> ConversationItem:
    """
    Async: Create a new item in a conversation.

    Args:
        conversation_id: The ID of the conversation to add the item to.
        type: The type of item (e.g., "message", "function_call", "function_call_output").
        role: The role of the item creator (e.g., "user", "assistant", "system").
        content: The content of the item.
        extra_headers: Additional headers to send with the request.
        extra_query: Additional query parameters to send with the request.
        extra_body: Additional body parameters to send with the request.
        timeout: Request timeout.
        custom_llm_provider: The LLM provider to use (defaults to "openai").
        api_key: API key for the provider.
        api_base: Base URL for the API.
        **kwargs: Additional arguments.

    Returns:
        ConversationItem: The created conversation item.
    """
    local_vars = locals()
    try:
        loop = asyncio.get_event_loop()
        kwargs["acreate_conversation_item"] = True

        func = partial(
            create_conversation_item,
            conversation_id=conversation_id,
            type=type,
            role=role,
            content=content,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            custom_llm_provider=custom_llm_provider,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )

        ctx = contextvars.copy_context()
        func_with_context = partial(ctx.run, func)
        init_response = await loop.run_in_executor(None, func_with_context)

        if asyncio.iscoroutine(init_response):
            response = await init_response
        else:
            response = init_response

        return response
    except Exception as e:
        raise litellm.exception_type(
            model="",
            custom_llm_provider=custom_llm_provider or "openai",
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


@client
def create_conversation_item(
    conversation_id: str,
    type: str,
    role: Optional[str] = None,
    content: Optional[List[ConversationContentItem]] = None,
    # Use the following arguments if you need to pass additional parameters to the API
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs,
) -> ConversationItem:
    """
    Sync: Create a new item in a conversation.

    Args:
        conversation_id: The ID of the conversation to add the item to.
        type: The type of item (e.g., "message", "function_call", "function_call_output").
        role: The role of the item creator (e.g., "user", "assistant", "system").
        content: The content of the item.
        extra_headers: Additional headers to send with the request.
        extra_query: Additional query parameters to send with the request.
        extra_body: Additional body parameters to send with the request.
        timeout: Request timeout.
        custom_llm_provider: The LLM provider to use (defaults to "openai").
        api_key: API key for the provider.
        api_base: Base URL for the API.
        **kwargs: Additional arguments.

    Returns:
        ConversationItem: The created conversation item.
    """
    from litellm.llms.openai.conversations import OpenAIConversationsAPI

    _is_async = kwargs.pop("acreate_conversation_item", False) is True

    # Default to OpenAI if no provider specified
    if custom_llm_provider is None:
        custom_llm_provider = "openai"

    openai_conversations_api = OpenAIConversationsAPI()

    if _is_async:
        return openai_conversations_api.acreate_conversation_item(
            conversation_id=conversation_id,
            type=type,
            role=role,
            content=content,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )
    else:
        return openai_conversations_api.create_conversation_item(
            conversation_id=conversation_id,
            type=type,
            role=role,
            content=content,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )


@client
async def alist_conversation_items(
    conversation_id: str,
    limit: Optional[int] = None,
    order: Optional[Literal["asc", "desc"]] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    # Use the following arguments if you need to pass additional parameters to the API
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs,
) -> ConversationItemList:
    """
    Async: List items in a conversation.

    Args:
        conversation_id: The ID of the conversation.
        limit: Maximum number of items to return.
        order: Sort order ("asc" or "desc").
        after: Return items after this ID (for pagination).
        before: Return items before this ID (for pagination).
        extra_headers: Additional headers to send with the request.
        extra_query: Additional query parameters to send with the request.
        extra_body: Additional body parameters to send with the request.
        timeout: Request timeout.
        custom_llm_provider: The LLM provider to use (defaults to "openai").
        api_key: API key for the provider.
        api_base: Base URL for the API.
        **kwargs: Additional arguments.

    Returns:
        ConversationItemList: List of conversation items.
    """
    local_vars = locals()
    try:
        loop = asyncio.get_event_loop()
        kwargs["alist_conversation_items"] = True

        func = partial(
            list_conversation_items,
            conversation_id=conversation_id,
            limit=limit,
            order=order,
            after=after,
            before=before,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            custom_llm_provider=custom_llm_provider,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )

        ctx = contextvars.copy_context()
        func_with_context = partial(ctx.run, func)
        init_response = await loop.run_in_executor(None, func_with_context)

        if asyncio.iscoroutine(init_response):
            response = await init_response
        else:
            response = init_response

        return response
    except Exception as e:
        raise litellm.exception_type(
            model="",
            custom_llm_provider=custom_llm_provider or "openai",
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


@client
def list_conversation_items(
    conversation_id: str,
    limit: Optional[int] = None,
    order: Optional[Literal["asc", "desc"]] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    # Use the following arguments if you need to pass additional parameters to the API
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs,
) -> ConversationItemList:
    """
    Sync: List items in a conversation.

    Args:
        conversation_id: The ID of the conversation.
        limit: Maximum number of items to return.
        order: Sort order ("asc" or "desc").
        after: Return items after this ID (for pagination).
        before: Return items before this ID (for pagination).
        extra_headers: Additional headers to send with the request.
        extra_query: Additional query parameters to send with the request.
        extra_body: Additional body parameters to send with the request.
        timeout: Request timeout.
        custom_llm_provider: The LLM provider to use (defaults to "openai").
        api_key: API key for the provider.
        api_base: Base URL for the API.
        **kwargs: Additional arguments.

    Returns:
        ConversationItemList: List of conversation items.
    """
    from litellm.llms.openai.conversations import OpenAIConversationsAPI

    _is_async = kwargs.pop("alist_conversation_items", False) is True

    # Default to OpenAI if no provider specified
    if custom_llm_provider is None:
        custom_llm_provider = "openai"

    openai_conversations_api = OpenAIConversationsAPI()

    if _is_async:
        return openai_conversations_api.alist_conversation_items(
            conversation_id=conversation_id,
            limit=limit,
            order=order,
            after=after,
            before=before,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )
    else:
        return openai_conversations_api.list_conversation_items(
            conversation_id=conversation_id,
            limit=limit,
            order=order,
            after=after,
            before=before,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )


@client
async def aget_conversation_item(
    conversation_id: str,
    item_id: str,
    # Use the following arguments if you need to pass additional parameters to the API
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs,
) -> ConversationItem:
    """
    Async: Retrieve a specific item from a conversation.

    Args:
        conversation_id: The ID of the conversation.
        item_id: The ID of the item to retrieve.
        extra_headers: Additional headers to send with the request.
        extra_query: Additional query parameters to send with the request.
        extra_body: Additional body parameters to send with the request.
        timeout: Request timeout.
        custom_llm_provider: The LLM provider to use (defaults to "openai").
        api_key: API key for the provider.
        api_base: Base URL for the API.
        **kwargs: Additional arguments.

    Returns:
        ConversationItem: The retrieved conversation item.
    """
    local_vars = locals()
    try:
        loop = asyncio.get_event_loop()
        kwargs["aget_conversation_item"] = True

        func = partial(
            get_conversation_item,
            conversation_id=conversation_id,
            item_id=item_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            custom_llm_provider=custom_llm_provider,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )

        ctx = contextvars.copy_context()
        func_with_context = partial(ctx.run, func)
        init_response = await loop.run_in_executor(None, func_with_context)

        if asyncio.iscoroutine(init_response):
            response = await init_response
        else:
            response = init_response

        return response
    except Exception as e:
        raise litellm.exception_type(
            model="",
            custom_llm_provider=custom_llm_provider or "openai",
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


@client
def get_conversation_item(
    conversation_id: str,
    item_id: str,
    # Use the following arguments if you need to pass additional parameters to the API
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs,
) -> ConversationItem:
    """
    Sync: Retrieve a specific item from a conversation.

    Args:
        conversation_id: The ID of the conversation.
        item_id: The ID of the item to retrieve.
        extra_headers: Additional headers to send with the request.
        extra_query: Additional query parameters to send with the request.
        extra_body: Additional body parameters to send with the request.
        timeout: Request timeout.
        custom_llm_provider: The LLM provider to use (defaults to "openai").
        api_key: API key for the provider.
        api_base: Base URL for the API.
        **kwargs: Additional arguments.

    Returns:
        ConversationItem: The retrieved conversation item.
    """
    from litellm.llms.openai.conversations import OpenAIConversationsAPI

    _is_async = kwargs.pop("aget_conversation_item", False) is True

    # Default to OpenAI if no provider specified
    if custom_llm_provider is None:
        custom_llm_provider = "openai"

    openai_conversations_api = OpenAIConversationsAPI()

    if _is_async:
        return openai_conversations_api.aget_conversation_item(
            conversation_id=conversation_id,
            item_id=item_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )
    else:
        return openai_conversations_api.get_conversation_item(
            conversation_id=conversation_id,
            item_id=item_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )


@client
async def adelete_conversation_item(
    conversation_id: str,
    item_id: str,
    # Use the following arguments if you need to pass additional parameters to the API
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs,
) -> ConversationDeletedResource:
    """
    Async: Delete a specific item from a conversation.

    Args:
        conversation_id: The ID of the conversation.
        item_id: The ID of the item to delete.
        extra_headers: Additional headers to send with the request.
        extra_query: Additional query parameters to send with the request.
        extra_body: Additional body parameters to send with the request.
        timeout: Request timeout.
        custom_llm_provider: The LLM provider to use (defaults to "openai").
        api_key: API key for the provider.
        api_base: Base URL for the API.
        **kwargs: Additional arguments.

    Returns:
        ConversationDeletedResource: Confirmation of deletion.
    """
    local_vars = locals()
    try:
        loop = asyncio.get_event_loop()
        kwargs["adelete_conversation_item"] = True

        func = partial(
            delete_conversation_item,
            conversation_id=conversation_id,
            item_id=item_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            custom_llm_provider=custom_llm_provider,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )

        ctx = contextvars.copy_context()
        func_with_context = partial(ctx.run, func)
        init_response = await loop.run_in_executor(None, func_with_context)

        if asyncio.iscoroutine(init_response):
            response = await init_response
        else:
            response = init_response

        return response
    except Exception as e:
        raise litellm.exception_type(
            model="",
            custom_llm_provider=custom_llm_provider or "openai",
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


@client
def delete_conversation_item(
    conversation_id: str,
    item_id: str,
    # Use the following arguments if you need to pass additional parameters to the API
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs,
) -> ConversationDeletedResource:
    """
    Sync: Delete a specific item from a conversation.

    Args:
        conversation_id: The ID of the conversation.
        item_id: The ID of the item to delete.
        extra_headers: Additional headers to send with the request.
        extra_query: Additional query parameters to send with the request.
        extra_body: Additional body parameters to send with the request.
        timeout: Request timeout.
        custom_llm_provider: The LLM provider to use (defaults to "openai").
        api_key: API key for the provider.
        api_base: Base URL for the API.
        **kwargs: Additional arguments.

    Returns:
        ConversationDeletedResource: Confirmation of deletion.
    """
    from litellm.llms.openai.conversations import OpenAIConversationsAPI

    _is_async = kwargs.pop("adelete_conversation_item", False) is True

    # Default to OpenAI if no provider specified
    if custom_llm_provider is None:
        custom_llm_provider = "openai"

    openai_conversations_api = OpenAIConversationsAPI()

    if _is_async:
        return openai_conversations_api.adelete_conversation_item(
            conversation_id=conversation_id,
            item_id=item_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )
    else:
        return openai_conversations_api.delete_conversation_item(
            conversation_id=conversation_id,
            item_id=item_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )
