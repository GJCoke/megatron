declare namespace SystemManage {
  /** 角色类型 */
  type Role = Api.Common.CommonRecord<{
    /** 角色名称 */
    name: string
    /** 角色描述 */
    describe: string
    /** 路由列表 */
    menuIds: number[]
    /** 接口权限code列表 */
    interfaceCodes: string[]
    /** 按钮权限code列表 */
    buttonCodes: string[]
  }>

  /** 角色搜索参数 */
  type RoleSearchParams = CommonType.RecordNullable<Pick<Role, "status"> & Api.Common.KeywordSearchParams>

  type RoleEdit = { id?: number } & Pick<Role, "status" | "name" | "describe">

  type RoleUpdatePermission = Pick<Role, "id"> & Partial<Pick<Role, "menuIds" | "interfaceCodes" | "buttonCodes">>

  /** 角色列表 */
  type RoleList = Api.Common.PaginatingQueryRecord<Role>

  /** 所有角色的简化类型 */
  type AllRole = Pick<Role, "id" | "name" | "describe">

  /** 用户类型 */
  type User = Api.Common.CommonRecord<{
    /** 用户名称 */
    name: string
    /** 用户手机号 */
    mobile: string
    /** 用户邮箱 */
    email: string
    /** 用户角色 */
    roleId?: number | null
    /** 群组ID */
    affiliationId?: number | null
    /** 头像 */
    avatarUrl?: string | null
    /** 超管 */
    isAdmin: boolean
    /** 缓存信息 */
    resource?: object | null
    /** 权限信息 */
    roles: string[]
    /** 昵称 */
    username: string
  }>

  type UserEdit = { id?: number } & Pick<
    User,
    "name" | "mobile" | "email" | "roleId" | "affiliationId" | "avatarUrl" | "status"
  >

  type CreateUser = UserEdit & { password: string }

  /** 用户搜索参数 */
  type UserSearchParams = CommonType.RecordNullable<
    Pick<User, "status" | "affiliationId"> & Api.Common.KeywordSearchParams
  >

  /** 用户列表 */
  type UserList = Api.Common.PaginatingQueryRecord<User>

  /**
   * 菜单类型
   *
   * - 1: 目录
   * - 2: 菜单
   */
  type MenuType = 1 | 2

  type MenuPermissionType = "buttons" | "interfaces"

  /** 菜单权限 */
  type MenuPermission = {
    /** 按钮代码 用于控制按钮权限 */
    code: string
    /** 按钮描述 */
    description: string
  }

  type MenuPermissionTree = {
    /** 按钮代码 用于控制按钮权限 */
    key: string
    /** 按钮描述 */
    label: string
    value: string
    disabled?: boolean
    selectable?: boolean
    children: MenuPermissionTree[]
  }

  /**
   * 图标类型
   *
   * - 1: 使用 iconify 图标
   * - 2: 使用本地图标
   */
  type IconType = 1 | 2

  /** 路由菜单的属性 */
  type MenuPropsOfRoute = Pick<
    import("vue-router").RouteMeta,
    | "i18nKey"
    | "keepAlive"
    | "constant"
    | "order"
    | "href"
    | "hideInMenu"
    | "activeMenu"
    | "multiTab"
    | "fixedIndexInTab"
    | "query"
    | "homepage"
  >

  type MenuInfo = {
    /** 父菜单 ID */
    nodeId: number
    /** 菜单类型 */
    menuType: MenuType
    /** 菜单名称 */
    menuName: string
    /** 路由名称 */
    routeName: string
    /** 路由路径 */
    routePath: string
    /** 组件 */
    component?: string
    /** iconify 图标名称或本地图标名称 */
    icon: string
    /** 图标类型 */
    iconType: IconType
    /** 按钮权限 */
    buttons?: MenuPermission[] | null
    /** 接口权限 */
    interfaces?: MenuPermission[] | null
    /** 子菜单 */
    children?: Menu[] | null
  }

  /** 菜单类型 */
  type Menu = Api.Common.CommonRecord<MenuInfo> & MenuPropsOfRoute

  type MenuEdit = {
    id?: number
  } & MenuInfo &
    MenuPropsOfRoute

  /** 菜单列表 */
  type MenuList = Api.Common.PaginatingQueryRecord<Menu>

  /** 菜单树结构 */
  type MenuTree = {
    /** 菜单 ID */
    id: number
    /** 菜单标签 */
    menuName: string
    /** 父菜单 ID */
    nodeId: number
    /** 子菜单树 */
    children?: MenuTree[]
  }

  type AffiliationInfo = {
    name: string
    nodeId: number
  }

  type AffiliationEdit = {
    id?: number
  } & AffiliationInfo

  type AffiliationTree = {
    id: number
    name: string
    nodeId: number
    children: AffiliationTree[]
  }
}
