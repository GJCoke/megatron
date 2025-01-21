# _author: Coke
# _date: 2025/1/9 下午4:18
# _description:
from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.auth.jwt import validate_permission
from src.models import ResponseModel
from src.models.types import DeleteRequestModel, Pagination

from ..auth.service import get_current_user
from ..manage.models import UserResponse
from .models import ProjectInfoResponse
from .service import delete_project, edit_project, get_project_list
from .types import BusinessEditProjectRequest, BusinessGetProjectListRequest

router = APIRouter(prefix="/business", dependencies=[Depends(validate_permission)])


@router.post("/getProjectList")
async def project_list(
    body: BusinessGetProjectListRequest, current_user: Annotated[UserResponse, Depends(get_current_user)]
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


@router.put("/editProjectInfo")
async def project_edit(
    body: BusinessEditProjectRequest,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> ResponseModel[ProjectInfoResponse]:
    """
    创建/修改 项目信息接口

    根据提供的项目 ID 更新项目信息, 如果项目ID不存在则创建新的项目。\f

    :param body: 包含项目信息的 <BusinessEditProjectRequest> 对象
    :param current_user: 当前的用户信息
    :return: 更新后的 <ProjectInfoResponse> 对象
    """

    project = await edit_project(
        current_user=current_user,
        project_id=body.id,
        name=body.name,
        describe=body.describe,
        driver_type=body.driverType,
        visibility=body.visibility,
        user_ids=body.userIds,
    )

    return ResponseModel(data=project)


@router.delete("/deleteProject")
async def project_delete(
    body: DeleteRequestModel, current_user: Annotated[UserResponse, Depends(get_current_user)]
) -> ResponseModel[ProjectInfoResponse]:
    """
    删除项目信息接口

    根据项目 ID 删除指定的项目信息。\f

    :param body: 包含项目 ID 的 <DeleteRequestModel> 对象
    :param current_user: 当前用户信息
    :return: 包含被删除项目信息的 <ResponseModel> 对象
    """

    project = await delete_project(current_user=current_user, project_id=body.id)
    return ResponseModel(data=project)
