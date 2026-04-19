from app.email_verify.utils import EmailVerifyUtils
from app.email_verify.config import get_service_settings, ServiceSettings
from fastapi import Depends
from functools import lru_cache


@lru_cache
def get_email_verify_utils(
    settings: ServiceSettings = Depends(get_service_settings),
) -> EmailVerifyUtils:
    return EmailVerifyUtils(settings.CODE_LENGTH)
