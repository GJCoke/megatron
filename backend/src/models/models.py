# _author: Coke
# _date: 2024/7/28 00:56
# _description: 基础数据库模型

from sqlmodel import Field, Relationship

from src.api.business.models import ProjectBase
from src.api.manage.models import AffiliationBase, MenuBase, RoleBase, UserPassword
from src.models import BaseNoCommonModel


class RoleTable(RoleBase, table=True):
    """角色数据库模型"""

    __tablename__ = "test_role"

    id: int | None = Field(None, primary_key=True, description="ID")
    users: list["UserTable"] = Relationship(back_populates="role")


class AffiliationTable(AffiliationBase, table=True):
    """人员归属数据库模型"""

    __tablename__ = "test_affiliation"

    id: int | None = Field(None, primary_key=True)
    users: list["UserTable"] = Relationship(back_populates="affiliation")


class UserProjectLink(BaseNoCommonModel, table=True):
    """项目和用户之间的中间表"""

    __tablename__ = "user_project_link"

    userId: int = Field(foreign_key="test_user.id", primary_key=True)
    projectId: int = Field(foreign_key="test_project.id", primary_key=True)


class UserTable(UserPassword, table=True):
    """用户数据库模型"""

    __tablename__ = "test_user"

    id: int | None = Field(None, primary_key=True)
    role: RoleTable | None = Relationship(back_populates="users")  # 角色信息
    affiliation: AffiliationTable | None = Relationship(back_populates="users")
    projects: list["ProjectTable"] = Relationship(back_populates="users", link_model=UserProjectLink)


class MenuTable(MenuBase, table=True):
    """菜单数据库模型"""

    __tablename__ = "test_menu"

    id: int | None = Field(None, primary_key=True, description="菜单ID")


class ProjectTable(ProjectBase, table=True):
    """项目数据库模型"""

    __tablename__ = "test_project"

    id: int | None = Field(None, primary_key=True, description="ID")
    users: list["UserTable"] = Relationship(back_populates="projects", link_model=UserProjectLink)
