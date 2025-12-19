from typing import Annotated

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from utils.templates import templates
from crud import users as crud_users

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/", name="users:list")
async def users_list(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    users = await crud_users.get_all_users(session=session)
    return templates.TemplateResponse(
        request=request,
        name="users/list.html",
        context={"users": users},
    )
