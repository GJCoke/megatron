import { transformRecordToOption } from "@/utils/common"

export const enableStatusRecord: Record<Api.Common.EnableStatus, string> = {
  1: "启用",
  2: "禁用"
}

export const enableStatusOptions = [
  {
    label: "启用",
    value: true
  },
  {
    label: "禁用",
    value: false
  }
]

export const menuTypeRecord: Record<SystemManage.MenuType, string> = {
  1: "目录",
  2: "菜单"
}

export const driverTypeRecord: Record<SystemProject.DriverType, string> = {
  1: "Selenium",
  2: "Appium"
}

export const visibilityRecord: Record<SystemProject.Visibility, string> = {
  0: "公开",
  1: "私有"
}

export const menuTypeOptions = transformRecordToOption(menuTypeRecord)

export const menuIconTypeRecord: Record<SystemManage.IconType, string> = {
  1: "iconify图标",
  2: "本地图标"
}

export const menuIconTypeOptions = transformRecordToOption(menuIconTypeRecord)

export const driverTypeOptions = transformRecordToOption(driverTypeRecord)

export const visibilityOptions = transformRecordToOption(visibilityRecord)
