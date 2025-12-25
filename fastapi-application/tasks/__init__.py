__all__ = ("send_welcome_email",)

import sys

import logging

from core.config import settings
from .welcome_email_notification import send_welcome_email

print(sys.argv)
if sys.argv[0] == "worker":
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.logging.log_format,
    )
