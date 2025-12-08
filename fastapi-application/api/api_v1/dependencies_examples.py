from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Header,
)

from utils.helper import GreatHelper, GreatService
from .dependencies.func_dep import (
    get_x_foo_bar,
    get_header_dependency,
    get_great_helper,
)

from .dependencies.cls_deps import (
    path_reader,
    PathReaderDependency,
    TokenIntrospectModel,
    access_required,
)

from core.config import settings

router = APIRouter(tags=["Dependencies Examples"], prefix=settings.api.v1.deps)

# header_x_foo_bar= Header(alias="x-foo-bar")


@router.get("/single-direct-dependency")
def single_direct_dependency(
    foobar: Annotated[
        str,
        Header(),
    ],
):
    return {
        "foobar": foobar,
        "message": "single-direct dependency is working",
    }


@router.get("/single-via-func")
def single_via_func(
    foobar: Annotated[
        str,
        Depends(get_x_foo_bar),
    ],
):
    return {
        "x-foobar": foobar,
        "message": "single-via-func is working",
    }


@router.get("/multi-direct-and-via-func")
def multi_direct_and_via_func(
    fizzbuzz: Annotated[
        str,
        Header(alias="x-fizz-buzz"),
    ],
    foobar: Annotated[
        str,
        Depends(get_x_foo_bar),
    ],
):
    return {
        "x-fizz-buzz": fizzbuzz,
        "x-foobar": foobar,
        "message": "multi-direct and-via-func is working",
    }


@router.get("/multi-indirect")
def multi_indirect_dependencies(
    foobar: Annotated[
        str,
        Depends(get_header_dependency("x-foobar")),
    ],
    fizzbuzz: Annotated[
        str,
        Depends(
            get_header_dependency(
                "x-fizz-buzz",
                default_value="FizzBuzz",
            )
        ),
    ],
):
    return {
        "x-fizz-buzz": fizzbuzz,
        "x-foobar": foobar,
        "message": "multi-indirect dependencies is working",
    }


@router.get("/top-level-helper-creation")
def top_level_helper_creation(
    helper_name: Annotated[
        str,
        Depends(
            get_header_dependency(
                "x-helper-name",
                default_value="HelperOne",
            )
        ),
    ],
    helper_default: Annotated[
        str,
        Depends(
            get_header_dependency(
                "x-helper-default",
                default_value="HelperTwo",
            )
        ),
    ],
):
    helper = GreatHelper(
        name=helper_name,
        default=helper_default,
    )
    return {
        "helper": helper.as_dict(),
        "message": "Top level helper creation",
    }


@router.get("/helper-as-dependency")
def helper_as_dependency(helper: Annotated[GreatHelper, Depends(get_great_helper)]):
    return {
        "helper": helper.as_dict(),
        "message": "helper-as-dependency is working",
    }


@router.get("/greate-service-as-dependency")
def greate_service_as_dependency(
    service: Annotated[
        GreatService,
        Depends(GreatService),
    ],
):
    return {
        "service": service.as_dict(),
        "message": "greate-service-as-dependency is working",
    }


@router.get("/path-reader-dependency-from-method")
def path_reader_dependency(
    reader: Annotated[
        PathReaderDependency,
        # Depends(path_reader.as_dependency),
        Depends(PathReaderDependency(source="direct/bar").as_dependency),
    ],
):
    return {
        "reader": reader.read(foo="bar"),
        "message": "path-reader dependency is working",
    }


@router.get("/direct-cls-dependency")
def direct_cls_dependency(
    token_data: Annotated[
        TokenIntrospectModel,
        Depends(access_required),
    ],
):
    return {
        "token_data": token_data.model_dump(),
        "message": "direct-cls-dependency is working",
    }
