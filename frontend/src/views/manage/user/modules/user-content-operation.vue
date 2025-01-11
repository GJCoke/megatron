<script setup lang="tsx">
import { NButton, NPopconfirm, NTag } from "naive-ui"
import { watch } from "vue"
import { batchDeleteUserInfo, deleteUserInfo, fetchGetUserList } from "@/service/api"
import { enableStatusRecord } from "@/constants/business"
import { useTable, useTableOperate } from "@/hooks/common/table"
import { useAuth } from "@/hooks/business/auth"
import { useAuthStore } from "@/store/modules/auth"
import { useAppStore } from "@/store/modules/app"
import UserOperateDrawer from "./user-operate-drawer.vue"
import UserSearch from "./user-search.vue"

defineOptions({
  name: "UserContentOperation"
})

interface Props {
  nodeId: number | null
}

const props = defineProps<Props>()

const appStore = useAppStore()
const { hasAuth } = useAuth()
const { userInfo } = useAuthStore()

const canAdd = hasAuth("manage.user.add")
const canEdit = hasAuth("manage.user.edit")
const canDelete = hasAuth("manage.user.delete")
const canBatchDelete = hasAuth("manage.user.batchDelete")

const {
  columns,
  columnChecks,
  data,
  getData,
  getDataByPage,
  loading,
  mobilePagination,
  searchParams,
  resetSearchParams
} = useTable({
  apiFn: fetchGetUserList,
  showTotal: true,
  apiParams: {
    page: 1,
    pageSize: 20,
    status: null,
    keyword: null,
    affiliationId: null
  },
  columns: () => {
    const baseColumns: NaiveUI.PermissionTableColumn<SystemManage.User>[] = [
      {
        type: "selection",
        align: "center",
        width: 48
      },
      {
        key: "index",
        title: "序号",
        align: "center",
        width: 64
      },
      {
        key: "name",
        title: "用户名称",
        align: "center",
        minWidth: 100
      },
      {
        key: "mobile",
        title: "手机号",
        align: "center",
        width: 120
      },
      {
        key: "email",
        title: "邮箱",
        align: "center",
        minWidth: 200
      },
      {
        key: "status",
        title: "用户状态",
        align: "center",
        width: 100,
        render: (row) => {
          if (row.status === null) {
            return null
          }

          const status = row.status ? 1 : 2
          const tagMap: Record<Api.Common.EnableStatus, NaiveUI.ThemeColor> = {
            1: "success",
            2: "warning"
          }

          const label = enableStatusRecord[status]

          return <NTag type={tagMap[status]}>{label}</NTag>
        }
      }
    ]

    /** 如果操作列无权限时不添加操作列 */
    if (canEdit || canDelete) {
      baseColumns.push({
        key: "operate",
        title: "操作",
        align: "center",
        width: 130,
        render: (row) => {
          /** 如果当前用户不是超管并且 row 用户是超管时无法编辑 */
          if (row.isAdmin && !userInfo.isAdmin) return null

          return (
            <div class="flex-center gap-8px">
              {canEdit && (
                <NButton type="primary" ghost size="small" onClick={() => edit(row.id)}>
                  编辑
                </NButton>
              )}
              {canDelete && (
                <NPopconfirm onPositiveClick={() => handleDelete(row.id)}>
                  {{
                    default: () => "确认删除吗？",
                    trigger: () => (
                      <NButton type="error" ghost size="small">
                        删除
                      </NButton>
                    )
                  }}
                </NPopconfirm>
              )}
            </div>
          )
        }
      })
    }

    return baseColumns
  }
})

const {
  drawerVisible,
  operateType,
  editingData,
  handleAdd,
  handleEdit,
  checkedRowKeys,
  onBatchDeleted,
  onDeleted
  // closeDrawer
} = useTableOperate(data, getData)

watch(
  () => props.nodeId,
  (newValue) => {
    searchParams.affiliationId = newValue
    getDataByPage()
  }
)

/** 批量删除 */
async function handleBatchDelete() {
  const { error } = await batchDeleteUserInfo(checkedRowKeys.value)

  if (!error) {
    await onBatchDeleted()
  }
}

/** 删除 */
async function handleDelete(id: number) {
  const { error } = await deleteUserInfo(id)

  if (!error) {
    await onDeleted()
  }
}

function edit(id: number) {
  handleEdit(id)
}
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <UserSearch v-model:model="searchParams" @reset="resetSearchParams" @search="getDataByPage" />
    <NCard title="用户列表" :bordered="false" size="small" class="sm:flex-1-hidden card-wrapper">
      <template #header-extra>
        <TableHeaderOperation
          v-model:columns="columnChecks"
          :disabled-delete="checkedRowKeys.length === 0"
          :loading="loading"
          :can-add="canAdd"
          :can-batch-delete="canBatchDelete"
          @add="handleAdd"
          @delete="handleBatchDelete"
          @refresh="getData"
        />
      </template>
      <NDataTable
        v-model:checked-row-keys="checkedRowKeys"
        :columns="columns"
        :data="data"
        size="small"
        :flex-height="!appStore.isMobile"
        :scroll-x="962"
        :loading="loading"
        remote
        :row-key="(row) => row.id"
        :pagination="mobilePagination"
        class="sm:h-full"
      />
      <UserOperateDrawer
        v-model:visible="drawerVisible"
        :node-id="nodeId"
        :operate-type="operateType"
        :row-data="editingData"
        @submitted="getDataByPage"
      />
    </NCard>
  </div>
</template>

<style scoped></style>
