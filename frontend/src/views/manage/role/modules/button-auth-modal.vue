<script setup lang="ts">
import { computed, ref, shallowRef, watch } from "vue"
import { editRolePermissionInfo, getPermissionMenuList } from "@/service/api"
import { addIsLeafToTreeNodes } from "@/utils/common"

defineOptions({
  name: "ButtonAuthModal"
})

interface Props {
  /** the roleId */
  roleId: number
  type: SystemManage.MenuPermissionType
  checked?: string[]
}

const props = defineProps<Props>()

interface Emits {
  (e: "submitted", role: SystemManage.Role): void
}

const emit = defineEmits<Emits>()

const visible = defineModel<boolean>("visible", {
  default: false
})

function closeModal() {
  visible.value = false
}

const title = computed(() => (props.type === "buttons" ? "按钮" : "接口"))

const tree = shallowRef<SystemManage.MenuPermissionTree[]>([])

async function getAllButtons() {
  // request
  const { data } = await getPermissionMenuList(props.type)
  tree.value = data || []
}

const checks = shallowRef<string[]>([])

function getChecks() {
  checks.value = props.checked || []
}

async function handleSubmit() {
  const body: SystemManage.RoleUpdatePermission = {
    id: props.roleId
  }

  if (props.type === "buttons") {
    body.buttonCodes = checks.value
  }

  if (props.type === "interfaces") {
    body.interfaceCodes = checks.value
  }

  const { error, data } = await editRolePermissionInfo(body)

  if (!error) {
    window.$message?.success?.("修改成功")
    emit("submitted", data)
    closeModal()
  }
}

/** 获取所有节点的 key 值 */
function getAllKeys(nodes: SystemManage.MenuPermissionTree[]) {
  const keys: string[] = []

  const traverse = (nodeList: SystemManage.MenuPermissionTree[]) => {
    nodeList.forEach((node) => {
      if (node.selectable) {
        keys.push(node.value)
      }

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
  getAllButtons()
  getChecks()
}

watch(visible, (val) => {
  if (val) {
    init()
  }
})
</script>

<template>
  <NModal v-model:show="visible" :title="`编辑${title}权限`" preset="card" class="w-480px">
    <div class="mb-4 border-b p-2">
      <NCheckbox @update:checked="handleUpdateChecked">{{ checkText }}</NCheckbox>
    </div>
    <NTree
      v-model:checked-keys="checks"
      :data="addIsLeafToTreeNodes(tree)"
      key-field="value"
      label-field="label"
      show-line
      block-line
      checkable
      expand-on-click
      virtual-scroll
      default-expand-all
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
