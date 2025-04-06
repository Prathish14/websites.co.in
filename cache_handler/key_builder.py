from typing import Any, Awaitable, Callable, Optional
from typing import Optional, Callable
from fastapi import Response, Request
import hashlib


def key_builder(func: Callable, namespace: Optional[str] = "",
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Optional[tuple] = None, kwargs: Optional[dict] = None) -> str:

    if func.__name__ in ('get_the_user_details'):
        cache_key_str = f'{kwargs["user_id"]}'

    prefix = f"local:{func.__name__}:{cache_key_str}"

    cache_key = (
        prefix
        + hashlib.md5(  # nosec:B303
            cache_key_str.encode()
        ).hexdigest()
    )
    return cache_key