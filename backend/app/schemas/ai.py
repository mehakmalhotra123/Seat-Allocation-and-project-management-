from typing import Any

from pydantic import BaseModel, Field


class AIQueryRequest(BaseModel):
    query: str = Field(
        min_length=2,
        max_length=500,
    )


class AIQueryResponse(BaseModel):
    answer: str

    intent: str

    data: dict[str, Any] | None = None

    requires_confirmation: bool = False