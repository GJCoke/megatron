declare namespace SystemProject {
  type Visibility = 0 | 1

  type DriverType = 1 | 2

  type ProjectInfo = {
    /** 项目名称 */
    name: string
    /** 项目描述 */
    describe?: string
    /** 驱动类型 */
    driverType: DriverType
    /** 是否公开 */
    visibility: Visibility
    /** 不公开时可见的用户 */
    users: SystemManage.UserBriefInfo[]
  }
  /** 项目类型 */
  type Project = Api.Common.CommonRecord<ProjectInfo>

  type ProjectEdit = {
    id?: number
    userIds?: number[]
  } & Pick<ProjectInfo, "name" | "driverType" | "visibility" | "describe">

  type RoleSearchParams = CommonType.RecordNullable<Api.Common.KeywordSearchParams>

  type ProjectList = Api.Common.PaginatingQueryRecord<Project>
}
