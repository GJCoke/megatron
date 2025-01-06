<script setup lang="ts">
import { shallowRef, watch, ref } from "vue"
import { editRolePermissionInfo, fetchGetMenuTree } from "@/service/api"
import { addIsLeafToTreeNodes } from "@/utils/common"

defineOptions({
  name: "MenuAuthModal"
})

interface Props {
  /** the roleId */
  roleId: number
  checked?: number[]
}

interface Emits {
  (e: "submitted", role: SystemManage.Role): void
}

const emit = defineEmits<Emits>()

const props = defineProps<Props>()

const visible = defineModel<boolean>("visible", {
  default: false
})

function closeModal() {
  visible.value = false
}

const tree = shallowRef<SystemManage.MenuTree[]>([])

async function getTree() {
  const { error, data } = await fetchGetMenuTree()

  if (!error) {
    tree.value = data
  }
}

const checks = shallowRef<number[]>([])

function getChecks() {
  checks.value = props.checked || []
}

async function handleSubmit() {
  const { error, data } = await editRolePermissionInfo({ menuIds: checks.value, id: props.roleId })

  if (!error) {
    window.$message?.success?.("修改成功")
    emit("submitted", data)
    closeModal()
  }
}

/** 获取所有节点的 key 值 */
function getAllKeys(nodes: SystemManage.MenuTree[]) {
  const keys: number[] = []

  const traverse = (nodeList: SystemManage.MenuTree[]) => {
    nodeList.forEach((node) => {
      keys.push(node.id)

      if (node.children) {
        traverse(node.children)
      }
    })
  }
  traverse(nodes)
  return keys
}

const checkText = ref<string>("全选")

/** 全选 */
function checkAll() {
  checks.value = getAllKeys(tree.value)
}

/** 取消全选 */
function uncheckAll() {
  checks.value = []
}

function handleUpdateChecked(value: boolean) {
  value ? checkAll() : uncheckAll()
  checkText.value = !value ? "全选" : "取消全选"
}

function init() {
  getTree()
  getChecks()
}

watch(visible, (val) => {
  if (val) {
    init()
  }
})
</script>

<template>
  <NModal v-model:show="visible" title="编辑菜单权限" preset="card" class="w-480px">
    <div class="mb-4 border-b p-2">
      <NCheckbox @update:checked="handleUpdateChecked">{{ checkText }}</NCheckbox>
    </div>
    <NTree
      v-model:checked-keys="checks"
      :data="addIsLeafToTreeNodes(tree)"
      key-field="id"
      label-field="menuName"
      checkable
      expand-on-click
      virtual-scroll
      default-expand-all
      show-line
      block-line
      class="h-280px"
    />
    <template #footer>
      <NSpace justify="end">
        <NButton size="small" class="mt-16px" @click="closeModal">取消</NButton>
        <NButton type="primary" size="small" class="mt-16px" @click="handleSubmit">确认</NButton>
      </NSpace>
    </template>
  </NModal>
</template>

<style scoped></style>
