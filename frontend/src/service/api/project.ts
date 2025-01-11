import { request } from "../request"

/**
 * 获取项目列表
 *
 * @returns 返回角色列表的请求结果
 */
export function fetchGetProjectList(data?: SystemProject.RoleSearchParams) {
  return request<SystemProject.ProjectList>({
    url: "/business/getProjectList",
    method: "POST",
    data
  })
}
