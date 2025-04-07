from pydantic import BaseModel
from typing import Optional


class RequestedInput(BaseModel):
    template_input: Optional[str] = None
    layout_input: Optional[str] = None
    content_input: Optional[str] = None
