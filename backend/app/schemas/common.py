from typing import Annotated
from pydantic import AfterValidator, HttpUrl

def _url_to_str(value: HttpUrl) -> str:
    text = str(value)
    if len(text) > 500:
        raise ValueError("URL must be at most 500 characters")
    return text

ImageUrl = Annotated[HttpUrl, AfterValidator(_url_to_str)]