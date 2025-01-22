from typing import Any, Optional

from pydantic import BaseModel, Field


class StandardResponse(BaseModel):
    status: bool = Field(
        ..., description="Indicates success (true) or failure (false)."
    )
    message: Optional[str] = Field(
        None, description="A descriptive message about the response."
    )
    data: Optional[Any] = Field(
        None, description="The payload data for success responses."
    )
    error: Optional[Any] = Field(
        None, description="Details about an error if one occurred."
    )


def success_response(
    message: Optional[str] = "Success",
    data: Optional[Any] = None,
) -> StandardResponse:
    return StandardResponse(status=True, message=message, data=data, error=None)


def error_response(
    message: Optional[str] = "An error occurred",
    error: Optional[Any] = None,
    data: Optional[Any] = None,
) -> StandardResponse:
    return StandardResponse(
        status=False,
        message=message,
        data=data,
        error=error,
    )
