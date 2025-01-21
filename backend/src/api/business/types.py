# _author: Coke
# _date: 2025/1/9 下午4:18
# _description: 项目管理相关请求模型

from fastapi import Body
from pydantic import field_validator

from src.models import CustomModel, GeneralKeywordPageRequestModel

DRIVER_SELENIUM = 1  # Selenium
DRIVER_APPIUM = 2  # Appium

PUBLIC = 0  # 公开
PRIVATE = 1  # 私有


class BusinessGetProjectListRequest(GeneralKeywordPageRequestModel):
    """获取项目列表"""


class BusinessEditProjectRequest(CustomModel):
    """修改项目请求"""

    id: int = Body(0, description="项目ID")
    name: str = Body(..., description="项目名称")
    describe: str = Body(None, description="项目描述")
    driverType: int = Body(..., description="项目驱动类型")
    visibility: int = Body(..., description="项目是否可见")
    userIds: list[int] = Body(None, description="如非公开项目则指定可见的用户id列表")

    # noinspection PyNestedDecorators
    @field_validator("driverType", mode="after")
    @classmethod
    def valid_driver_type(cls, driver_type: int) -> int:
        if driver_type not in (DRIVER_APPIUM, DRIVER_SELENIUM):
            raise ValueError("项目驱动类型错误")

        return driver_type

    # noinspection PyNestedDecorators
    @field_validator("visibility", mode="after")
    @classmethod
    def valid_visibility(cls, visibility: int) -> int:
        if visibility not in (PUBLIC, PRIVATE):
            raise ValueError("项目可见类型错误")

        return visibility
