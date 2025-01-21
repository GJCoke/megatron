# _author: Coke
# _date: 2025/1/9 下午4:18
# _description:

from sqlmodel import or_, select

from src import database
from src.api.manage.models import UserResponse
from src.models.models import ProjectTable, UserProjectLink, UserTable
from src.models.types import Pagination

from ..auth.exceptions import AuthorizationFailed
from .types import DRIVER_SELENIUM, PRIVATE, PUBLIC


async def get_project_list(
    page: int, size: int, *, current_user: UserResponse, keyword: str = ""
) -> Pagination[list[ProjectTable]]:
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
            or_(UserProjectLink.userId == current_user.id, ProjectTable.visibility == PUBLIC),
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


async def check_user_permission(user: UserResponse, project: ProjectTable) -> None:
    """
    检查当前用户是否拥有此项目的访问权限
    """
    if project.visibility == PUBLIC:
        return

    user_ids = [item.id for item in project.users]
    if user.id not in user_ids:
        raise AuthorizationFailed()


async def edit_project(
    *,
    current_user: UserResponse,
    project_id: int,
    name: str,
    describe: str = None,
    driver_type: int = DRIVER_SELENIUM,
    visibility: int = PUBLIC,
    user_ids: list[int] | None = None,
) -> ProjectTable:
    """
    创建/更新一个项目

    该函数根据`project_id` 来判断是否创建还是修改

    :param current_user: 当前用户信息
    :param project_id: 项目 ID
    :param name: 项目名称
    :param describe: 项目描述
    :param driver_type: 项目驱动类型
    :param visibility: 是否可见
    :param user_ids: 如项目非公开时可访问的用户列表
    """

    # 如果项目为公开或者 user_ids 为 None 时赋值一个新列表
    if user_ids is None or visibility == PUBLIC:
        user_ids = []

    # 如果可访问列表中无存在用户则将自己添加到其中
    if visibility == PRIVATE and not user_ids:
        user_ids.append(current_user.id)

    # 如果 用户列表存在数据则将其 ID 转换为用户表信息数据
    users_list = []
    if user_ids:
        users_list = await database.select_all(
            select(UserTable).where(or_(*[UserTable.id == user_id for user_id in user_ids]))
        )

    if project_id:
        project = await database.select(
            select(ProjectTable).options(database.joined_load(ProjectTable.users)).where(ProjectTable.id == project_id)
        )

        await check_user_permission(current_user, project)

        project.name = name
        project.describe = describe
        project.driverType = driver_type
        project.visibility = visibility

        # 清空多对多实例  这里有问题, 应该只需要一次提交但是不清楚为什么不可行
        project.users.clear()
        await database.update(project)

        # 重新添加
        project.users.extend(users_list)
        update_project = await database.update(project)
        return update_project

    add_project = await database.insert(
        ProjectTable,
        ProjectTable(name=name, describe=describe, driverType=driver_type, visibility=visibility, users=users_list),
    )
    return add_project


async def delete_project(*, current_user: UserResponse, project_id: int) -> ProjectTable:
    """
    删除一个项目信息

    该函数根据 `project_id` 删除指定的项目信息。

    :param current_user: 当前用户信息
    :param project_id: 项目 ID
    :return: 删除的项目信息的响应对象
    """
    select_project = await database.select(
        select(ProjectTable).options(database.joined_load(ProjectTable.users)).where(ProjectTable.id == project_id)
    )
    await check_user_permission(current_user, select_project)

    project = await database.delete(select(ProjectTable).where(ProjectTable.id == project_id))
    return project
