import logging

from fastapi_users import BaseUserManager, IntegerIDMixin

from core.models import User
from core.config import settings
from core.types.user_id import UserIdType
from fastapi import Request

from utils.webhooks.user import send_new_user_notification

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: Request | None = None,
    ):
        log.warning(
            "User %r has registered.",
            user.id,
        )

        # new action: send webhook
        await send_new_user_notification(user)

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Request | None = None,
    ):
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Request | None = None,
    ):
        log.warning(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )
