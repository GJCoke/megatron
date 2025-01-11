declare namespace SystemProject {
  /** 项目类型 */
  type Project = Api.Common.CommonRecord<{
    /** 项目名称 */
    name: string
    /** 项目描述 */
    describe: string
    /** 驱动类型 */
    driverType: string
    /** 是否公开 */
    visibility: number
    /** 不公开时可见的用户 */
    users: SystemManage.UserBriefInfo[]
  }>

  type RoleSearchParams = CommonType.RecordNullable<Api.Common.KeywordSearchParams>

  type ProjectList = Api.Common.PaginatingQueryRecord<Project>
}
