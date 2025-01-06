# _author: Coke
# _date: 2024/9/14 上午10:16
# _description:

from sqlmodel import Session

from src.api.auth.security import hash_password
from src.api.manage.models import MenuTable, UserTable, AffiliationTable
from src.api.manage.types import ICON_ICONIFY, MENU_DIRECTORY, MENU_ROUTE


def menu(session: Session) -> None:
    """
    默认菜单
    :param session:
    :return:
    """

    constant_menus: list[MenuTable] = [
        MenuTable(
            component="layout.blank$view.403",
            menuName="403",
            menuType=MENU_ROUTE,
            routeName="403",
            routePath="/403",
            iconType=ICON_ICONIFY,
            icon="ic:baseline-block",
            status=True,
            hideInMenu=True,
            constant=True,
            homepage=False,
        ),
        MenuTable(
            component="layout.blank$view.404",
            menuName="404",
            menuType=MENU_ROUTE,
            routeName="404",
            routePath="/404",
            iconType=ICON_ICONIFY,
            icon="ic:baseline-web-asset-off",
            status=True,
            hideInMenu=True,
            constant=True,
            homepage=False,
        ),
        MenuTable(
            component="layout.blank$view.500",
            menuName="500",
            menuType=MENU_ROUTE,
            routeName="500",
            routePath="/500",
            iconType=ICON_ICONIFY,
            icon="ic:baseline-wifi-off",
            status=True,
            hideInMenu=True,
            constant=True,
            homepage=False,
        ),
        MenuTable(
            component="layout.base$view.iframe-page",
            menuName="框架页面",
            menuType=MENU_ROUTE,
            routeName="iframe-page",
            routePath="/iframe-page/:url",
            iconType=ICON_ICONIFY,
            icon="material-symbols:iframe",
            status=True,
            hideInMenu=True,
            constant=True,
            homepage=False,
        ),
        MenuTable(
            component="layout.blank$view.login",
            menuName="登录",
            menuType=MENU_ROUTE,
            routeName="login",
            routePath="/login/:module(pwd-login|code-login|register|reset-pwd|bind-wechat)?",
            iconType=ICON_ICONIFY,
            icon="ant-design:login-outlined",
            status=True,
            hideInMenu=True,
            constant=True,
            homepage=False,
        ),
    ]

    _manage = MenuTable(
        component="layout.home",
        menuName="系统管理",
        menuType=MENU_DIRECTORY,
        routeName="manage",
        routePath="/manage",
        iconType=ICON_ICONIFY,
        icon="carbon:cloud-service-management",
    )

    parent_menu = [_manage]

    session.add_all(constant_menus + parent_menu)
    session.commit()
    user_menus: list[MenuTable] = [
        MenuTable(
            component="view.manage_menu",
            menuName="菜单管理",
            menuType=MENU_ROUTE,
            routeName="manage_menu",
            routePath="/manage/menu",
            iconType=ICON_ICONIFY,
            icon="material-symbols:route",
            nodeId=_manage.id,  # type: ignore
            interfaces=[
                dict(code="/manage/getMenuList", description="获取菜单列表接口"),  # type: ignore
                dict(code="/manage/editMenuInfo", description="新增/修改菜单接口"),  # type: ignore
                dict(code="/manage/deleteMenu", description="删除菜单接口"),  # type: ignore
                dict(code="/manage/batchDeleteMenu", description="批量删除菜单接口"),  # type: ignore
                dict(code="/manage/getPageAll", description="获取当前所有的页面"),  # type: ignore
                dict(code="/manage/getRouterMenuAll", description="获取简化后的路由菜单列表"),  # type: ignore
                dict(code="/manage/getPermissionMenuAll", description="通过菜单类型获取对应的列表"),  # type: ignore
            ],
            buttons=[
                dict(code="manage.menu.add", description="添加菜单"),  # type: ignore
                dict(code="manage.menu.addChild", description="添加子菜单"),  # type: ignore
                dict(code="manage.menu.edit", description="编辑菜单"),  # type: ignore
                dict(code="manage.menu.delete", description="删除菜单"),  # type: ignore
                dict(code="manage.menu.batchDelete", description="批量删除菜单"),  # type: ignore
            ],
        ),
        MenuTable(
            component="view.manage_role",
            menuName="角色管理",
            menuType=MENU_ROUTE,
            routeName="manage_role",
            routePath="/manage/role",
            iconType=ICON_ICONIFY,
            icon="carbon:user-role",
            nodeId=_manage.id,  # type: ignore
            interfaces=[
                dict(code="/manage/editRoleInfo", description="新增/修改角色信息"),  # type: ignore
                dict(code="/manage/updateRolePermission", description="更新当前角色的权限信息"),  # type: ignore
                dict(code="/manage/getRoleList", description="获取角色列表接口"),  # type: ignore
                dict(code="/manage/getRoleAll", description="获取全部角色列表接口"),  # type: ignore
                dict(code="/manage/deleteRole", description="删除角色信息接口"),  # type: ignore
                dict(code="/manage/batchDeleteRole", description="批量删除角色信息接口"),  # type: ignore
            ],
            buttons=[
                dict(code="manage.role.add", description="添加角色"),  # type: ignore
                dict(code="manage.role.edit", description="编辑角色"),  # type: ignore
                dict(code="manage.role.delete", description="删除角色"),  # type: ignore
                dict(code="manage.role.batchDelete", description="批量删除角色"),  # type: ignore
            ],
        ),
        MenuTable(
            component="view.manage_user",
            menuName="用户管理",
            menuType=MENU_ROUTE,
            routeName="manage_user",
            routePath="/manage/user",
            iconType=ICON_ICONIFY,
            icon="ic:round-manage-accounts",
            nodeId=_manage.id,  # type: ignore
            interfaces=[
                dict(code="/manage/createUser", description="新增用户信息"),  # type: ignore
                dict(code="/manage/updateUserInfo", description="修改用户信息"),  # type: ignore
                dict(code="/manage/updateUserPassword", description="修改用户密码"),  # type: ignore
                dict(code="/manage/getUserList", description="获取用户列表"),  # type: ignore
                dict(code="/manage/deleteUser", description="删除用户信息"),  # type: ignore
                dict(code="/manage/batchDeleteUser", description="批量删除用户信息"),  # type: ignore
                dict(code="/manage/editAffiliationInfo", description="新增/修改群组信息"),  # type: ignore
                dict(code="/manage/getAffiliationList", description="获取群组信息列表"),  # type: ignore
                dict(code="/manage/deleteAffiliation", description="删除群组信息"),  # type: ignore
            ],
            buttons=[
                dict(code="manage.user.add", description="添加角色"),  # type: ignore
                dict(code="manage.user.edit", description="编辑角色"),  # type: ignore
                dict(code="manage.user.delete", description="删除角色"),  # type: ignore
                dict(code="manage.user.batchDelete", description="批量删除角色"),  # type: ignore
                dict(code="manage.affiliation.add", description="添加群组"),  # type: ignore
                dict(code="manage.affiliation.edit", description="编辑群组"),  # type: ignore
                dict(code="manage.affiliation.delete", description="删除群组"),  # type: ignore
                dict(code="manage.affiliation.addChild", description="添加子群组"),  # type: ignore
            ],
        )
    ]

    session.add_all(user_menus)
    session.commit()


def affiliation(session: Session) -> None:
    company_structure = dict(
        name="霸天集团",
        children=[
            dict(
                name="机械部队",
                children=[dict(name="机甲小队"), dict(name="机器人兵团"), dict(name="战车队")]
            ),
            dict(
                name="战略部",
                children=[dict(name="情报分析组"), dict(name="指挥决策组")]
            ),
            dict(
                name="科技部",
                children=[dict(name="高能武器组"), dict(name="人工智能组")]
            ),
            dict(
                name="资源部",
                children=[dict(name="矿产采集组"), dict(name="能源管理组")]
            ),
            dict(
                name="后勤部",
                children=[dict(name="物资供应组"), dict(name="人员调度组")]
            )
        ]
    )

    _corporation = AffiliationTable(
        name=company_structure["name"]
    )
    session.add(_corporation)
    session.commit()

    def recursion(children: list, node_id: int):

        for item in children:
            _item = AffiliationTable(
                name=item["name"],
                nodeId=node_id
            )
            session.add(_item)
            session.commit()

            if item.get("children"):
                recursion(item["children"], _item.id)

    recursion(company_structure["children"], _corporation.id)


def user(session: Session) -> None:
    """
    默认用户
    :param session:
    :return:
    """

    users: list[UserTable] = [
        UserTable(
            name="超级管理员",
            username="SupperAdmin",
            email="admin@gmail.cn",
            mobile="18888888888",
            password=hash_password("admin123"),
            isAdmin=True,
        )
    ]

    session.add_all(users)
    session.commit()


def manage(session: Session) -> None:
    """
    系统管理相关的默认数据, 用于初始化数据库
    :param session:
    :return:
    """

    menu(session)
    user(session)
    affiliation(session)
