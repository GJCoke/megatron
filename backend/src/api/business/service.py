# _author: Coke
# _date: 2025/1/9 下午4:18
# _description:

from sqlmodel import or_, select

from src import database
from src.api.manage.models import UserResponse
from src.models.models import ProjectTable, UserProjectLink
from src.models.types import Pagination

from .models import ProjectInfoResponse


async def get_project_list(
    page: int, size: int, *, current_user: UserResponse, keyword: str = ""
) -> Pagination[list[ProjectInfoResponse]]:
    """
    获取项目信息列表

    分页获取项目信息, 并根据 `keyword` 进行关键字匹配

    :param page: 当前页
    :param size: 每页的大小
    :param current_user: 当前用户信息
    :param keyword: 关键字查询
    :return: 项目信息列表
    """

    select_statement = (
        select(ProjectTable)
        .options(database.joined_load(ProjectTable.users))
        .join(
            UserProjectLink,
            UserProjectLink.projectId == ProjectTable.id,  # type: ignore
            isouter=True,
        )
        .where(
            or_(UserProjectLink.userId == current_user.id, ProjectTable.visibility == 0),
            database.like(field=ProjectTable.name, keyword=keyword),
        )
    )

    project_list = await database.pagination(
        select_statement,
        page=page,
        size=size,
    )

    return Pagination(
        page=project_list.page,
        pageSize=project_list.pageSize,
        records=project_list.records,
        total=project_list.total,
    )
