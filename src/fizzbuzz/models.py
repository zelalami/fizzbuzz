from typing import Annotated

from pydantic import BaseModel, Field


class FizzBuzzParams(BaseModel):
    factor1: int
    factor2: int
    limit: Annotated[int, Field(strict=True, le=100)]  # Ensure limit <= 100
    replacement1: str
    replacement2: str
