from pydantic import BaseModel, Field

class ResponseModel(BaseModel):
    """Schema for standardized API responses.

    Attributes:
        status: Status of the response, either 'success' or 'failure'.
        data: Payload of the response, can be any type.
    """
    status: str = Field(..., description="Status of the response, either 'success' or 'failure'")
    data: dict | list | str | int | float | None = Field(..., description="Payload of the response, can be any type")