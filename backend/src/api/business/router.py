# _author: Coke
# _date: 2025/1/9 下午4:18
# _description:
from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.auth.jwt import validate_permission
from src.models import ResponseModel
from src.models.types import GeneralKeywordPageRequestModel, Pagination

from ..auth.service import get_current_user
from ..manage.models import UserResponse
from .models import ProjectInfoResponse
from .service import get_project_list

router = APIRouter(prefix="/business", dependencies=[Depends(validate_permission)])


@router.post("/getProjectList")
async def project_list(
    body: GeneralKeywordPageRequestModel, current_user: Annotated[UserResponse, Depends(get_current_user)]
) -> ResponseModel[Pagination[list[ProjectInfoResponse]]]:
    """
    获取项目列表接口

    获取项目的分页列表，可以通过关键字进行过滤。\f

    :param body: 包含分页和关键字信息的 <GeneralKeywordPageRequestModel> 对象
    :param current_user: 当前用户信息
    :return: 包含项目列表的 <ResponseModel> 对象
    """

    project = await get_project_list(body.page, body.pageSize, keyword=body.keyword, current_user=current_user)
    return ResponseModel(data=project)
