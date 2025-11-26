"""
Conversations API Proxy Endpoints

This module provides FastAPI endpoints for the Conversations API,
which is part of the OpenAI Responses API ecosystem for managing
stateful multi-turn conversations.

Endpoints:
- POST /v1/conversations - Create a new conversation
- GET /v1/conversations/{conversation_id} - Retrieve a conversation
- POST /v1/conversations/{conversation_id} - Update a conversation
- DELETE /v1/conversations/{conversation_id} - Delete a conversation
- POST /v1/conversations/{conversation_id}/items - Create a conversation item
- GET /v1/conversations/{conversation_id}/items - List conversation items
- GET /v1/conversations/{conversation_id}/items/{item_id} - Get a conversation item
- DELETE /v1/conversations/{conversation_id}/items/{item_id} - Delete a conversation item
"""

from fastapi import APIRouter, Depends, Request, Response

from litellm.proxy._types import *
from litellm.proxy.auth.user_api_key_auth import UserAPIKeyAuth, user_api_key_auth
from litellm.proxy.common_request_processing import ProxyBaseLLMRequestProcessing

router = APIRouter()


####### CONVERSATION ENDPOINTS ###################


@router.post(
    "/v1/conversations",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
@router.post(
    "/conversations",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
@router.post(
    "/openai/v1/conversations",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
async def create_conversation(
    request: Request,
    fastapi_response: Response,
    user_api_key_dict: UserAPIKeyAuth = Depends(user_api_key_auth),
):
    """
    Create a new conversation.

    This is part of the OpenAI Responses API ecosystem for managing stateful
    multi-turn conversations.

    ```bash
    curl -X POST http://localhost:4000/v1/conversations \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer sk-1234" \
    -d '{
        "metadata": {"user_id": "user123"}
    }'
    ```
    """
    from litellm.proxy.proxy_server import (
        _read_request_body,
        general_settings,
        llm_router,
        proxy_config,
        proxy_logging_obj,
        select_data_generator,
        user_api_base,
        user_max_tokens,
        user_model,
        user_request_timeout,
        user_temperature,
        version,
    )

    data = await _read_request_body(request=request)
    processor = ProxyBaseLLMRequestProcessing(data=data)
    try:
        return await processor.base_process_llm_request(
            request=request,
            fastapi_response=fastapi_response,
            user_api_key_dict=user_api_key_dict,
            route_type="acreate_conversation",
            proxy_logging_obj=proxy_logging_obj,
            llm_router=llm_router,
            general_settings=general_settings,
            proxy_config=proxy_config,
            select_data_generator=select_data_generator,
            model=None,
            user_model=user_model,
            user_temperature=user_temperature,
            user_request_timeout=user_request_timeout,
            user_max_tokens=user_max_tokens,
            user_api_base=user_api_base,
            version=version,
        )
    except Exception as e:
        raise await processor._handle_llm_api_exception(
            e=e,
            user_api_key_dict=user_api_key_dict,
            proxy_logging_obj=proxy_logging_obj,
            version=version,
        )


@router.get(
    "/v1/conversations/{conversation_id}",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
@router.get(
    "/conversations/{conversation_id}",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
@router.get(
    "/openai/v1/conversations/{conversation_id}",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
async def get_conversation(
    conversation_id: str,
    request: Request,
    fastapi_response: Response,
    user_api_key_dict: UserAPIKeyAuth = Depends(user_api_key_auth),
):
    """
    Retrieve a conversation by ID.

    ```bash
    curl -X GET http://localhost:4000/v1/conversations/conv_abc123 \
    -H "Authorization: Bearer sk-1234"
    ```
    """
    from litellm.proxy.proxy_server import (
        _read_request_body,
        general_settings,
        llm_router,
        proxy_config,
        proxy_logging_obj,
        select_data_generator,
        user_api_base,
        user_max_tokens,
        user_model,
        user_request_timeout,
        user_temperature,
        version,
    )

    data = await _read_request_body(request=request)
    data["conversation_id"] = conversation_id
    processor = ProxyBaseLLMRequestProcessing(data=data)
    try:
        return await processor.base_process_llm_request(
            request=request,
            fastapi_response=fastapi_response,
            user_api_key_dict=user_api_key_dict,
            route_type="aget_conversation",
            proxy_logging_obj=proxy_logging_obj,
            llm_router=llm_router,
            general_settings=general_settings,
            proxy_config=proxy_config,
            select_data_generator=select_data_generator,
            model=None,
            user_model=user_model,
            user_temperature=user_temperature,
            user_request_timeout=user_request_timeout,
            user_max_tokens=user_max_tokens,
            user_api_base=user_api_base,
            version=version,
        )
    except Exception as e:
        raise await processor._handle_llm_api_exception(
            e=e,
            user_api_key_dict=user_api_key_dict,
            proxy_logging_obj=proxy_logging_obj,
            version=version,
        )


@router.post(
    "/v1/conversations/{conversation_id}",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
@router.post(
    "/conversations/{conversation_id}",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
@router.post(
    "/openai/v1/conversations/{conversation_id}",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
async def update_conversation(
    conversation_id: str,
    request: Request,
    fastapi_response: Response,
    user_api_key_dict: UserAPIKeyAuth = Depends(user_api_key_auth),
):
    """
    Update a conversation.

    ```bash
    curl -X POST http://localhost:4000/v1/conversations/conv_abc123 \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer sk-1234" \
    -d '{
        "metadata": {"status": "completed"}
    }'
    ```
    """
    from litellm.proxy.proxy_server import (
        _read_request_body,
        general_settings,
        llm_router,
        proxy_config,
        proxy_logging_obj,
        select_data_generator,
        user_api_base,
        user_max_tokens,
        user_model,
        user_request_timeout,
        user_temperature,
        version,
    )

    data = await _read_request_body(request=request)
    data["conversation_id"] = conversation_id
    processor = ProxyBaseLLMRequestProcessing(data=data)
    try:
        return await processor.base_process_llm_request(
            request=request,
            fastapi_response=fastapi_response,
            user_api_key_dict=user_api_key_dict,
            route_type="aupdate_conversation",
            proxy_logging_obj=proxy_logging_obj,
            llm_router=llm_router,
            general_settings=general_settings,
            proxy_config=proxy_config,
            select_data_generator=select_data_generator,
            model=None,
            user_model=user_model,
            user_temperature=user_temperature,
            user_request_timeout=user_request_timeout,
            user_max_tokens=user_max_tokens,
            user_api_base=user_api_base,
            version=version,
        )
    except Exception as e:
        raise await processor._handle_llm_api_exception(
            e=e,
            user_api_key_dict=user_api_key_dict,
            proxy_logging_obj=proxy_logging_obj,
            version=version,
        )


@router.delete(
    "/v1/conversations/{conversation_id}",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
@router.delete(
    "/conversations/{conversation_id}",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
@router.delete(
    "/openai/v1/conversations/{conversation_id}",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
async def delete_conversation(
    conversation_id: str,
    request: Request,
    fastapi_response: Response,
    user_api_key_dict: UserAPIKeyAuth = Depends(user_api_key_auth),
):
    """
    Delete a conversation.

    ```bash
    curl -X DELETE http://localhost:4000/v1/conversations/conv_abc123 \
    -H "Authorization: Bearer sk-1234"
    ```
    """
    from litellm.proxy.proxy_server import (
        _read_request_body,
        general_settings,
        llm_router,
        proxy_config,
        proxy_logging_obj,
        select_data_generator,
        user_api_base,
        user_max_tokens,
        user_model,
        user_request_timeout,
        user_temperature,
        version,
    )

    data = await _read_request_body(request=request)
    data["conversation_id"] = conversation_id
    processor = ProxyBaseLLMRequestProcessing(data=data)
    try:
        return await processor.base_process_llm_request(
            request=request,
            fastapi_response=fastapi_response,
            user_api_key_dict=user_api_key_dict,
            route_type="adelete_conversation",
            proxy_logging_obj=proxy_logging_obj,
            llm_router=llm_router,
            general_settings=general_settings,
            proxy_config=proxy_config,
            select_data_generator=select_data_generator,
            model=None,
            user_model=user_model,
            user_temperature=user_temperature,
            user_request_timeout=user_request_timeout,
            user_max_tokens=user_max_tokens,
            user_api_base=user_api_base,
            version=version,
        )
    except Exception as e:
        raise await processor._handle_llm_api_exception(
            e=e,
            user_api_key_dict=user_api_key_dict,
            proxy_logging_obj=proxy_logging_obj,
            version=version,
        )


####### CONVERSATION ITEM ENDPOINTS ###################


@router.post(
    "/v1/conversations/{conversation_id}/items",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
@router.post(
    "/conversations/{conversation_id}/items",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
@router.post(
    "/openai/v1/conversations/{conversation_id}/items",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
async def create_conversation_item(
    conversation_id: str,
    request: Request,
    fastapi_response: Response,
    user_api_key_dict: UserAPIKeyAuth = Depends(user_api_key_auth),
):
    """
    Create a new item in a conversation.

    ```bash
    curl -X POST http://localhost:4000/v1/conversations/conv_abc123/items \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer sk-1234" \
    -d '{
        "type": "message",
        "role": "user",
        "content": [{"type": "input_text", "text": "Hello!"}]
    }'
    ```
    """
    from litellm.proxy.proxy_server import (
        _read_request_body,
        general_settings,
        llm_router,
        proxy_config,
        proxy_logging_obj,
        select_data_generator,
        user_api_base,
        user_max_tokens,
        user_model,
        user_request_timeout,
        user_temperature,
        version,
    )

    data = await _read_request_body(request=request)
    data["conversation_id"] = conversation_id
    processor = ProxyBaseLLMRequestProcessing(data=data)
    try:
        return await processor.base_process_llm_request(
            request=request,
            fastapi_response=fastapi_response,
            user_api_key_dict=user_api_key_dict,
            route_type="acreate_conversation_item",
            proxy_logging_obj=proxy_logging_obj,
            llm_router=llm_router,
            general_settings=general_settings,
            proxy_config=proxy_config,
            select_data_generator=select_data_generator,
            model=None,
            user_model=user_model,
            user_temperature=user_temperature,
            user_request_timeout=user_request_timeout,
            user_max_tokens=user_max_tokens,
            user_api_base=user_api_base,
            version=version,
        )
    except Exception as e:
        raise await processor._handle_llm_api_exception(
            e=e,
            user_api_key_dict=user_api_key_dict,
            proxy_logging_obj=proxy_logging_obj,
            version=version,
        )


@router.get(
    "/v1/conversations/{conversation_id}/items",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
@router.get(
    "/conversations/{conversation_id}/items",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
@router.get(
    "/openai/v1/conversations/{conversation_id}/items",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
async def list_conversation_items(
    conversation_id: str,
    request: Request,
    fastapi_response: Response,
    user_api_key_dict: UserAPIKeyAuth = Depends(user_api_key_auth),
):
    """
    List items in a conversation.

    ```bash
    curl -X GET http://localhost:4000/v1/conversations/conv_abc123/items \
    -H "Authorization: Bearer sk-1234"
    ```
    """
    from litellm.proxy.proxy_server import (
        _read_request_body,
        general_settings,
        llm_router,
        proxy_config,
        proxy_logging_obj,
        select_data_generator,
        user_api_base,
        user_max_tokens,
        user_model,
        user_request_timeout,
        user_temperature,
        version,
    )

    data = await _read_request_body(request=request)
    data["conversation_id"] = conversation_id
    processor = ProxyBaseLLMRequestProcessing(data=data)
    try:
        return await processor.base_process_llm_request(
            request=request,
            fastapi_response=fastapi_response,
            user_api_key_dict=user_api_key_dict,
            route_type="alist_conversation_items",
            proxy_logging_obj=proxy_logging_obj,
            llm_router=llm_router,
            general_settings=general_settings,
            proxy_config=proxy_config,
            select_data_generator=select_data_generator,
            model=None,
            user_model=user_model,
            user_temperature=user_temperature,
            user_request_timeout=user_request_timeout,
            user_max_tokens=user_max_tokens,
            user_api_base=user_api_base,
            version=version,
        )
    except Exception as e:
        raise await processor._handle_llm_api_exception(
            e=e,
            user_api_key_dict=user_api_key_dict,
            proxy_logging_obj=proxy_logging_obj,
            version=version,
        )


@router.get(
    "/v1/conversations/{conversation_id}/items/{item_id}",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
@router.get(
    "/conversations/{conversation_id}/items/{item_id}",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
@router.get(
    "/openai/v1/conversations/{conversation_id}/items/{item_id}",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
async def get_conversation_item(
    conversation_id: str,
    item_id: str,
    request: Request,
    fastapi_response: Response,
    user_api_key_dict: UserAPIKeyAuth = Depends(user_api_key_auth),
):
    """
    Retrieve a specific item from a conversation.

    ```bash
    curl -X GET http://localhost:4000/v1/conversations/conv_abc123/items/item_xyz789 \
    -H "Authorization: Bearer sk-1234"
    ```
    """
    from litellm.proxy.proxy_server import (
        _read_request_body,
        general_settings,
        llm_router,
        proxy_config,
        proxy_logging_obj,
        select_data_generator,
        user_api_base,
        user_max_tokens,
        user_model,
        user_request_timeout,
        user_temperature,
        version,
    )

    data = await _read_request_body(request=request)
    data["conversation_id"] = conversation_id
    data["item_id"] = item_id
    processor = ProxyBaseLLMRequestProcessing(data=data)
    try:
        return await processor.base_process_llm_request(
            request=request,
            fastapi_response=fastapi_response,
            user_api_key_dict=user_api_key_dict,
            route_type="aget_conversation_item",
            proxy_logging_obj=proxy_logging_obj,
            llm_router=llm_router,
            general_settings=general_settings,
            proxy_config=proxy_config,
            select_data_generator=select_data_generator,
            model=None,
            user_model=user_model,
            user_temperature=user_temperature,
            user_request_timeout=user_request_timeout,
            user_max_tokens=user_max_tokens,
            user_api_base=user_api_base,
            version=version,
        )
    except Exception as e:
        raise await processor._handle_llm_api_exception(
            e=e,
            user_api_key_dict=user_api_key_dict,
            proxy_logging_obj=proxy_logging_obj,
            version=version,
        )


@router.delete(
    "/v1/conversations/{conversation_id}/items/{item_id}",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
@router.delete(
    "/conversations/{conversation_id}/items/{item_id}",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
@router.delete(
    "/openai/v1/conversations/{conversation_id}/items/{item_id}",
    dependencies=[Depends(user_api_key_auth)],
    tags=["conversations"],
)
async def delete_conversation_item(
    conversation_id: str,
    item_id: str,
    request: Request,
    fastapi_response: Response,
    user_api_key_dict: UserAPIKeyAuth = Depends(user_api_key_auth),
):
    """
    Delete a specific item from a conversation.

    ```bash
    curl -X DELETE http://localhost:4000/v1/conversations/conv_abc123/items/item_xyz789 \
    -H "Authorization: Bearer sk-1234"
    ```
    """
    from litellm.proxy.proxy_server import (
        _read_request_body,
        general_settings,
        llm_router,
        proxy_config,
        proxy_logging_obj,
        select_data_generator,
        user_api_base,
        user_max_tokens,
        user_model,
        user_request_timeout,
        user_temperature,
        version,
    )

    data = await _read_request_body(request=request)
    data["conversation_id"] = conversation_id
    data["item_id"] = item_id
    processor = ProxyBaseLLMRequestProcessing(data=data)
    try:
        return await processor.base_process_llm_request(
            request=request,
            fastapi_response=fastapi_response,
            user_api_key_dict=user_api_key_dict,
            route_type="adelete_conversation_item",
            proxy_logging_obj=proxy_logging_obj,
            llm_router=llm_router,
            general_settings=general_settings,
            proxy_config=proxy_config,
            select_data_generator=select_data_generator,
            model=None,
            user_model=user_model,
            user_temperature=user_temperature,
            user_request_timeout=user_request_timeout,
            user_max_tokens=user_max_tokens,
            user_api_base=user_api_base,
            version=version,
        )
    except Exception as e:
        raise await processor._handle_llm_api_exception(
            e=e,
            user_api_key_dict=user_api_key_dict,
            proxy_logging_obj=proxy_logging_obj,
            version=version,
        )
