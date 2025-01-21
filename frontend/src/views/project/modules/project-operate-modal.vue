<script setup lang="tsx">
import { computed, reactive, ref, watch } from "vue"
import { NTag, NText } from "naive-ui"
import { useFormRules, useNaiveForm } from "@/hooks/common/form"
import { editProjectInfo } from "@/service/api/project"
import { driverTypeOptions, visibilityOptions } from "@/constants/business"
import { useLoading } from "~/packages/hooks"
import { fetchGetUserList } from "@/service/api"
import UserCommonAvatar from "@/components/common/user-common-avatar.vue"

defineOptions({
  name: "ProjectOperateModal"
})

interface Props {
  operateType: NaiveUI.TableOperateType
  rowData?: SystemProject.Project | null
}

const props = defineProps<Props>()

interface Emits {
  (e: "submitted", project: SystemProject.Project): void
}

const emit = defineEmits<Emits>()

const visible = defineModel<boolean>("visible", {
  default: false
})

const { formRef, validate, restoreValidation } = useNaiveForm()
const { defaultRequiredRule } = useFormRules()

/** 标题 */
const title = computed(() => {
  const titles: Record<NaiveUI.TableOperateType, string> = {
    add: "新增项目",
    edit: "编辑项目"
  }
  return titles[props.operateType]
})

const model: SystemProject.ProjectEdit = reactive(createDefaultModel())
const showUser = computed(() => model.visibility !== 0)

/** 创建默认对象 */
function createDefaultModel(): SystemProject.ProjectEdit {
  return {
    name: "",
    describe: "",
    driverType: 1,
    visibility: 0,
    id: undefined,
    userIds: []
  }
}
type RuleKey = Extract<keyof SystemProject.ProjectEdit, "name" | "driverType" | "visibility" | "userIds">

const rules: Record<RuleKey, App.Global.FormRule> = {
  name: defaultRequiredRule,
  driverType: defaultRequiredRule,
  visibility: defaultRequiredRule,
  userIds: defaultRequiredRule
}

/** 初始化 model 对象 */
function handleInitModel() {
  Object.assign(model, createDefaultModel())

  if (!props.rowData) return

  /** 编辑群组信息 */
  if (props.operateType === "edit") {
    const { users, ...rest } = props.rowData
    const userIds = users.map((item) => item.id)
    getUserList("", userIds)
    Object.assign(model, rest, { userIds })
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

const options = ref<SystemManage.User[]>([])

const { loading, startLoading, endLoading } = useLoading()

/** 获取用户列表 */
async function getUserList(query: string = "", userIds: number[] | undefined = undefined) {
  const { error, data } = await fetchGetUserList({ status: true, page: 1, pageSize: 10, keyword: query, userIds })
  options.value = error ? [] : data?.records
}

/** 查询函数 */
async function handleSearch(query: string) {
  startLoading()
  await getUserList(query)
  endLoading()
}

type RenderTagProps = {
  option: SystemManage.User
  handleClose: () => void
}

/** 自定义用户选择器的选中用户样式 */
function renderMultipleSelectTag({ option, handleClose }: RenderTagProps) {
  return (
    <NTag
      style={{ padding: "0 6px 0 4px" }}
      round
      closable
      onClose={(e) => {
        e.stopPropagation()
        handleClose()
      }}
    >
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "4px" }}>
        <UserCommonAvatar username={option.name} src={option.avatarUrl} />
        {option.name}
      </div>
    </NTag>
  )
}

/** 自定义用户选择器的样式 */
function renderLabel(option: SystemManage.User) {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center"
      }}
    >
      <UserCommonAvatar username={option.name} src={option.avatarUrl} />
      <div
        style={{
          marginLeft: "12px",
          padding: "4px 0"
        }}
      >
        <div>{option.name}</div>
        <NText depth={3} tag="div">
          {option.username}
        </NText>
      </div>
    </div>
  )
}

/** 提交表单 */
async function handleSubmit() {
  await validate()
  const { error, data } = await editProjectInfo(model)

  if (!error) {
    window.$message?.success("提交成功")
    closeModel()
    emit("submitted", data)
  }
}
</script>

<template>
  <NModal v-model:show="visible" :title="title" preset="card" class="w-480px">
    <NForm ref="formRef" :model="model" :rules="rules" :label-width="100">
      <NGrid responsive="screen" item-responsive>
        <NFormItemGi span="24 m:24" label="项目名称" path="name">
          <NInput v-model:value="model.name" placeholder="请输入项目名称" />
        </NFormItemGi>
        <NFormItemGi span="24 m:24" label="角色描述" path="describe">
          <NInput v-model:value="model.describe" placeholder="请输入项目描述" />
        </NFormItemGi>
        <NFormItemGi span="24 m:12" label="驱动类型" path="driverType">
          <NRadioGroup v-model:value="model.driverType">
            <NRadio v-for="item in driverTypeOptions" :key="item.value" :value="item.value" :label="item.label" />
          </NRadioGroup>
        </NFormItemGi>
        <NFormItemGi span="24 m:12" label="是否可见" path="visibility">
          <NRadioGroup v-model:value="model.visibility">
            <NRadio v-for="item in visibilityOptions" :key="item.value" :value="item.value" :label="item.label" />
          </NRadioGroup>
        </NFormItemGi>
        <NFormItemGi v-if="showUser" span="24 m:24" label="可见用户" path="userIds">
          <NSelect
            v-model:value="model.userIds"
            multiple
            filterable
            :options="options"
            :loading="loading"
            clearable
            remote
            :clear-filter-after-select="false"
            :render-label="renderLabel"
            :render-tag="renderMultipleSelectTag"
            label-field="name"
            value-field="id"
            placeholder="请选择可见的用户"
            max-tag-count="responsive"
            @search="handleSearch"
          />
        </NFormItemGi>
      </NGrid>
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
