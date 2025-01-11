<script setup lang="tsx">
import type { TreeOption } from "naive-ui"
import { NButton, NDropdown, useDialog } from "naive-ui"
import { type Ref, onMounted, ref } from "vue"
import { deleteAffiliationInfo } from "@/service/api"
import { useBoolean } from "~/packages/hooks"
import SvgIcon from "@/components/custom/svg-icon.vue"
import type { GroupTree } from "@/store/modules/affiliation"
import { useAffiliationStore } from "@/store/modules/affiliation"
import { useAuth } from "@/hooks/business/auth"
import AffiliationOperateModal, { type OperateType } from "./affiliation-operate-modal.vue"

defineOptions({
  name: "UserSideOperation"
})

const { bool: visible, setTrue: openModal } = useBoolean()

const affiliationStore = useAffiliationStore()
const { hasAuth } = useAuth()

const canAdd = hasAuth("manage.affiliation.add")
const canAddChild = hasAuth("manage.affiliation.addChild")
const canEdit = hasAuth("manage.affiliation.edit")
const canDelete = hasAuth("manage.affiliation.delete")

const operateType = ref<OperateType>("add")
const editingData: Ref<SystemManage.AffiliationEdit | null> = ref(null)

interface Emits {
  (e: "nodeClick", node: GroupTree): void
}

const emit = defineEmits<Emits>()

const pattern = ref<string>("")

function handleAdd() {
  operateType.value = "add"
  openModal()
}

function handleEdit(item: SystemManage.AffiliationEdit) {
  operateType.value = "edit"
  editingData.value = { ...item }
  openModal()
}

function handleAddChild(item: SystemManage.AffiliationEdit) {
  operateType.value = "addChild"
  editingData.value = { ...item }
  openModal()
}

const dialog = useDialog()

function handleDelete(id: number) {
  dialog.warning({
    title: "确认删除",
    content: "确认删除此群组吗？",
    positiveText: "确认",
    negativeText: "取消",
    negativeButtonProps: {
      size: "medium"
    },
    positiveButtonProps: {
      type: "primary",
      size: "medium"
    },
    onPositiveClick: async () => {
      await deleteAffiliationInfo(id)
      await affiliationStore.getUserAffiliationTree()
    }
  })
}

type Key = string | number
const hoveredNodeKey = ref<Key | undefined>(undefined)

/** 自定义渲染节点 当鼠标移入时显示更多按钮, 移出时销毁 监听下拉菜单是否打开, 如果打开则将更新当前 info 的 dropdownVisible 值 并为每个节点创建下拉菜单是否打开，如果打开则一直显示更多按钮, 否则销毁更多按钮 */
function renderLabel({ option: node }: { option: TreeOption }) {
  const handleMouseEnter = () => {
    hoveredNodeKey.value = node.key
  }

  const handleMouseLeave = () => {
    hoveredNodeKey.value = undefined
  }

  /** 点击下拉菜单中的 Item 时 */
  function dropdownChange(key: Key, option: GroupTree) {
    if (key === "addChild") {
      handleAddChild({ id: option.key, name: option.label, nodeId: option.nodeId })
    } else if (key === "edit") {
      handleEdit({ id: option.key, name: option.label, nodeId: option.nodeId })
    } else if (key === "delete") {
      handleDelete(option.key)
    }
  }

  /** 更多下拉菜单内容 */
  const moreOptions = []

  if (!canAddChild && !canEdit && !canDelete) return <div onClick={() => rowClick(node as GroupTree)}>{node.label}</div>

  if (canAddChild) {
    moreOptions.push({
      label: () => <span class="text-primary">添加子节点</span>,
      key: "addChild",
      icon: () => <SvgIcon icon="material-symbols:add" class="text-20px color-primary" />
    })
  }

  if (canEdit) {
    moreOptions.push({
      label: () => <span class="text-warning">编辑</span>,
      key: "edit",
      icon: () => <SvgIcon icon="material-symbols:edit-square-outline" class="text-16px color-warning" />
    })
  }

  if (canDelete) {
    moreOptions.push({
      label: () => <span class="text-error">删除</span>,
      key: "delete",
      icon: () => <SvgIcon icon="material-symbols:delete-outline-sharp" class="text-16px color-error" />
    })
  }

  return (
    <div
      onMouseenter={handleMouseEnter}
      onMouseleave={handleMouseLeave}
      onClick={() => rowClick(node as GroupTree)}
      class="flex items-center justify-between"
    >
      {node.label}
      {(hoveredNodeKey.value === node.key || node.dropdownVisible) && (
        <NDropdown
          onUpdateShow={(value: boolean) => (node.dropdownVisible = value)}
          trigger="hover"
          options={moreOptions}
          onSelect={(key: Key) => dropdownChange(key, node as GroupTree)}
        >
          <NButton quaternary circle size="tiny" type="primary" onClick={(e) => e.stopPropagation()}>
            <SvgIcon icon="ic:outline-more-horiz" />
          </NButton>
        </NDropdown>
      )}
    </div>
  )
}

/** 点击 Tree node 的事件 */
function rowClick(node: GroupTree) {
  emit("nodeClick", node)
}

onMounted(() => {
  affiliationStore.getUserAffiliationTree()
})
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-8px overflow-hidden lt-sm:overflow-auto">
    <NCard :bordered="false" size="small" class="card-wrapper">
      <div class="flex items-center gap-2">
        <NInput v-model:value="pattern" round placeholder="输入群组名称查询" size="small">
          <template #prefix>
            <SvgIcon icon="hugeicons:search-01" />
          </template>
        </NInput>
        <NButton v-if="canAdd" type="primary" round ghost size="small" @click="handleAdd">
          <template #icon>
            <SvgIcon icon="material-symbols:add" />
          </template>
          添加
        </NButton>
      </div>
    </NCard>
    <div class="sm:flex-1-hidden card-wrapper bg-card-box">
      <div class="h-full">
        <NScrollbar class="p-16px">
          <NSpin :show="affiliationStore.affiliationLoading">
            <NTree
              block-line
              :data="affiliationStore.affiliationTree"
              :pattern="pattern"
              default-expand-all
              :show-irrelevant-nodes="false"
              :selectable="false"
              :render-label="renderLabel"
            >
              <template #empty>
                <NEmpty class="h-400px flex items-center justify-center" description="暂无分组，快去添加一个吧~">
                  <template #extra>
                    <NButton v-if="canAdd" quaternary size="small" type="primary" @click="handleAdd">添加分组</NButton>
                  </template>
                </NEmpty>
              </template>
            </NTree>
          </NSpin>
        </NScrollbar>
      </div>
      <AffiliationOperateModal
        v-model:visible="visible"
        :operate-type="operateType"
        :row-data="editingData"
        @submitted="affiliationStore.getUserAffiliationTree"
      />
    </div>
  </div>
</template>

<style scoped></style>
