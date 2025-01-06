<script setup lang="ts">
import { computed, reactive, watch } from "vue"
import { useFormRules, useNaiveForm } from "@/hooks/common/form"
import { editUserAffiliationInfo } from "@/service/api"

defineOptions({
  name: "AffiliationOperateModal"
})

export type OperateType = NaiveUI.TableOperateType | "addChild"

interface Props {
  /** the type of operation */
  operateType: OperateType
  /** the edit menu data or the parent menu data when adding a child menu */
  rowData?: SystemManage.AffiliationEdit | null
}

const props = defineProps<Props>()

interface Emits {
  (e: "submitted"): void
}

const emit = defineEmits<Emits>()

const visible = defineModel<boolean>("visible", {
  default: false
})

const { formRef, validate, restoreValidation } = useNaiveForm()
const { defaultRequiredRule } = useFormRules()

/** 标题 */
const title = computed(() => {
  const titles: Record<OperateType, string> = {
    add: "新增群组",
    addChild: "新增子群组",
    edit: "编辑群组"
  }
  return titles[props.operateType]
})

const model: SystemManage.AffiliationEdit = reactive(createDefaultModel())

/** 创建默认对象 */
function createDefaultModel(): SystemManage.AffiliationEdit {
  return {
    name: "",
    nodeId: 0,
    id: undefined
  }
}
type RuleKey = Extract<keyof SystemManage.AffiliationInfo, "name">

const rules: Record<RuleKey, App.Global.FormRule> = {
  name: defaultRequiredRule
}

/** 初始化 model 对象 */
function handleInitModel() {
  Object.assign(model, createDefaultModel())

  if (!props.rowData) return

  /** 添加子群组 */
  if (props.operateType === "addChild") {
    Object.assign(model, {
      nodeId: props.rowData.id
    })
  }

  /** 编辑群组信息 */
  if (props.operateType === "edit") {
    const { ...rest } = props.rowData
    Object.assign(model, rest)
  }
}

/** 关闭弹窗 */
function closeModel() {
  visible.value = false
}

/** 监听 visible 的变化，当抽屉显示时初始化 model */
watch(visible, () => {
  if (visible.value) {
    handleInitModel()
    restoreValidation()
  }
})

/** 提交表单 */
async function handleSubmit() {
  await validate()
  const { error } = await editUserAffiliationInfo(model)

  if (!error) {
    window.$message?.success("提交成功")
    closeModel()
    emit("submitted")
  }
}
</script>

<template>
  <NModal v-model:show="visible" :title="title" preset="card" class="w-480px">
    <NForm ref="formRef" class="mt-2" :model="model" :rules="rules" :label-width="100">
      <NFormItem label="群组名称" path="name">
        <NInput v-model:value="model.name" placeholder="请输入群组名称" />
      </NFormItem>
    </NForm>
    <template #footer>
      <NSpace justify="end" :size="16">
        <NButton @click="closeModel">取消</NButton>
        <NButton type="primary" @click="handleSubmit">确认</NButton>
      </NSpace>
    </template>
  </NModal>
</template>

<style scoped></style>
