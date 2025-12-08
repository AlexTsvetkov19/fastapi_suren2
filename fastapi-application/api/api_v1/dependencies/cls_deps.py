from typing import Generator, Self, Annotated

from fastapi import Request, Header, HTTPException
from pydantic import BaseModel
from starlette import status


class PathReaderDependency:
    def __init__(self, source: str) -> None:
        self.source = source
        self._request: Request | None = None
        self._foobar: str = ""

    @property
    def path(self) -> str:
        if self._request is None:
            return ""
        return self._request.url.path

    def as_dependency(
        self,
        request: Request,
        foobar: Annotated[
            str,
            Header(alias="x-foobar"),
        ] = "foo",
    ) -> Generator[Self, None, None]:
        self._request = request
        self._foobar = foobar
        yield self
        self._request = None
        self._foobar: str = ""

    def read(self, **kwargs: str) -> dict[str, str]:
        return {
            "source": self.source,
            "path": self.path,
            "foobar": self._foobar,
            "kwargs": kwargs,
        }


path_reader = PathReaderDependency(source="abc/path/foo/bar")


class TokenData(BaseModel):
    id: int
    username: str


class TokenIntrospectModel(BaseModel):
    result: TokenData


class HeaderAccessDependency:
    def __init__(self, secret_token: str) -> None:
        self.secret_token = secret_token

    def validate(self, token: str) -> TokenIntrospectModel:
        if token != self.secret_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"token {token} is invalid",
            )
        return TokenIntrospectModel(
            result=TokenData(
                id=42,
                username="foobar",
            )
        )

    def __call__(
        self, token: Annotated[str, Header(alias="x-access-token")]
    ) -> TokenIntrospectModel:
        token_data = self.validate(token=token)
        # log.info("validated token", ...)
        return token_data


access_required = HeaderAccessDependency(secret_token="foo-bar-fizz-buzz")
