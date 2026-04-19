from typing import TypeAlias, Annotated, Any
from pydantic import AfterValidator, BeforeValidator
import re


def xss_injection_validate(field: str) -> str:
    xss_patterns = [
        r"<\s*script.*?>.*?<\s*/\s*script\s*>",
        r"<\s*(iframe|img|svg|meta|body|input|link|style|div|a|form|button)\W.*?>",
        r'<[^>]*\s(on\w+)\s*=\s*["\']?[^"\'<>]*["\']?[^>]*>',
        r"javascript:\s*\S+",
        r"data:\s*(text/html|text/javascript|application/x-shockwave-flash)",
        r"eval\s*\(",
    ]

    for pattern in xss_patterns:
        if re.search(pattern, field, re.IGNORECASE):
            raise ValueError("XSS threat detected in the entered data")
    return field


def string_whitespace_valid(field: Any) -> str:
    if not isinstance(field, str):
        raise ValueError("incorrect type")

    field = field.strip()
    if len(field) == 0:
        raise ValueError("incorrect field lenght")
    return field


Str: TypeAlias = Annotated[str, BeforeValidator(string_whitespace_valid)]
StrXSS: TypeAlias = Annotated[Str, AfterValidator(xss_injection_validate)]
