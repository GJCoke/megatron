# _author: Coke
# _date: 2025/1/9 下午4:18
# _description: 项目管理相关响应模型

from sqlmodel import Field

from src.api.manage.models import BriefUserInfoResponse
from src.models import GeneralBase

PUBLIC = 0  # 公开
PRIVATE = 1  # 私有


class ProjectBase(GeneralBase):
    """项目数据模型"""

    describe: str | None = Field(None, description="项目描述信息")
    driverType: str = Field(..., description="驱动类型")
    visibility: int = Field(0, description="项目可见是否公开")


class ProjectCreate(ProjectBase):
    """创建项目实例"""


class ProjectInfoResponse(ProjectBase):
    """项目响应实例"""

    id: int
    users: list[BriefUserInfoResponse] = []
