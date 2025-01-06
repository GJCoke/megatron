import { defineStore } from "pinia"
import { ref } from "vue"
import type { TreeOption } from "naive-ui"
import { SetupStoreId } from "@/enum"
import { getUserAffiliationList } from "@/service/api"
import { useLoading } from "~/packages/hooks"

export interface GroupTree extends TreeOption {
  key: number
  label: string
  nodeId: number
  dropdownVisible: boolean
}

export const useAffiliationStore = defineStore(SetupStoreId.Manage, () => {
  const { loading: affiliationLoading, startLoading, endLoading } = useLoading()
  const affiliationTree = ref<GroupTree[]>([])

  /** 更改树结构内容 */
  function affiliationOperate(affiliationList: SystemManage.AffiliationTree[]): GroupTree[] {
    return affiliationList.map((item) => ({
      key: item.id,
      label: item.name,
      nodeId: item.nodeId,
      dropdownVisible: false,
      children: item.children.length ? affiliationOperate(item.children) : undefined
    }))
  }

  /** 获取服务器数据 */
  async function getUserAffiliationTree() {
    startLoading()
    const affiliationList = await getUserAffiliationList()
    if (!affiliationList || !affiliationList.data) return

    affiliationTree.value = affiliationOperate(affiliationList.data)
    endLoading()
  }

  return {
    affiliationTree,
    affiliationLoading,
    getUserAffiliationTree
  }
})
