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

/**
 * 修改项目信息
 *
 * @returns 返回项目信息的请求结果
 */
export function editProjectInfo(data: SystemProject.ProjectEdit) {
  return request<SystemProject.Project>({
    url: "/business/editProjectInfo",
    method: "PUT",
    data
  })
}

/**
 * 删除项目
 *
 * @returns 返回删除后的项目
 */
export function deleteProjectInfo(id: number) {
  return request<SystemProject.Project>({
    url: "/business/deleteProject",
    method: "DELETE",
    data: { id }
  })
}
