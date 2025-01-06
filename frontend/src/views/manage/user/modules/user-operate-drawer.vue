<script setup lang="ts">
import { computed, reactive, ref, watch } from "vue"
import { useFormRules, useNaiveForm } from "@/hooks/common/form"
import { createUserInfo, fetchGetRoleAll, updateUserInfo } from "@/service/api"
import { enableStatusOptions } from "@/constants/business"
import { useAuthStore } from "@/store/modules/auth"
import { useAffiliationStore } from "@/store/modules/affiliation"

defineOptions({
  name: "UserOperateDrawer"
})

interface Props {
  /** the type of operation */
  operateType: NaiveUI.TableOperateType
  nodeId: number | null
  /** the edit row data */
  rowData?: SystemManage.User | null
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
const affiliationStore = useAffiliationStore()

const authStore = useAuthStore()

const title = computed(() => {
  const titles: Record<NaiveUI.TableOperateType, string> = {
    add: "添加用户",
    edit: "编辑用户"
  }
  return titles[props.operateType]
})

type PasswordModel = {
  password: string
  confirmPassword: string
}

type Model = SystemManage.UserEdit & PasswordModel

const model = reactive(createDefaultModel())

function createDefaultModel(): Model {
  return {
    name: "",
    mobile: "",
    email: "",
    roleId: null,
    status: true,
    password: "",
    confirmPassword: "",
    affiliationId: null,
    avatarUrl: null
  }
}

type RuleKey = Extract<keyof Model, "name" | "status" | "mobile" | "email" | "password" | "confirmPassword">

const rules = computed<Record<RuleKey, App.Global.FormRule[]>>(() => {
  const { defaultRequiredRule, formRules, createConfirmPwdRule } = useFormRules()

  return {
    name: [defaultRequiredRule],
    status: [defaultRequiredRule],
    mobile: formRules.phone,
    email: formRules.email,
    password: formRules.password,
    confirmPassword: createConfirmPwdRule(model.password)
  }
})

/** the enabled role options */
const roleOptions = ref<CommonType.Option<number>[]>([])

async function getRoleOptions() {
  const { error, data } = await fetchGetRoleAll()

  if (!error) {
    const options = data.map((item) => ({
      label: item.name,
      value: item.id
    }))

    roleOptions.value = [...options]
  }
}

function handleInitModel() {
  Object.assign(model, createDefaultModel())

  if (props.operateType === "add") {
    Object.assign(model, { affiliationId: props.nodeId })
  }

  if (props.operateType === "edit" && props.rowData) {
    Object.assign(model, props.rowData)
  }
}

function closeDrawer() {
  visible.value = false
}

async function handleSubmit() {
  await validate()
  const { confirmPassword: _confirmPassword, ...params } = model

  if (props.operateType === "add") {
    params.password = await authStore.encryptCipher(params.password)

    const { error } = await createUserInfo(params)
    if (error) return
  } else if (props.operateType === "edit") {
    const { password: _password, ...editParams } = params

    const { error } = await updateUserInfo(editParams)
    if (error) return
  }
  window.$message?.success("提交成功")
  closeDrawer()
  emit("submitted")
}

/** 限制手机号只能输入数字 */
function onlyAllowNumber(value: string) {
  return !value || /^\d+$/.test(value)
}

watch(visible, () => {
  if (visible.value) {
    handleInitModel()
    restoreValidation()
    getRoleOptions()
  }
})
</script>

<template>
  <NDrawer v-model:show="visible" display-directive="show" :width="360">
    <NDrawerContent :title="title" :native-scrollbar="false" closable>
      <NForm ref="formRef" :model="model" :rules="rules">
        <NFormItem label="用户名称" path="name">
          <NInput v-model:value="model.name" placeholder="请输入用户名称" />
        </NFormItem>
        <NFormItem label="手机号" path="mobile">
          <NInput
            v-model:value="model.mobile"
            maxlength="11"
            show-count
            :allow-input="onlyAllowNumber"
            placeholder="请输入手机号"
          />
        </NFormItem>
        <NFormItem label="邮箱" path="email">
          <NInput v-model:value="model.email" placeholder="请输入用户邮箱" />
        </NFormItem>
        <div v-if="operateType === 'add'">
          <NFormItem label="密码" path="password">
            <NInput
              v-model:value="model.password"
              :input-props="{ autocomplete: 'new-password' }"
              type="password"
              show-password-on="mousedown"
              placeholder="请输入用户密码"
            />
          </NFormItem>
          <NFormItem label="确认密码" path="confirmPassword">
            <NInput
              v-model:value="model.confirmPassword"
              :input-props="{ autocomplete: 'new-password' }"
              type="password"
              show-password-on="mousedown"
              placeholder="请再次输入用户密码"
            />
          </NFormItem>
        </div>
        <NFormItem label="用户状态" path="status">
          <NRadioGroup v-model:value="model.status">
            <NRadio v-for="item in enableStatusOptions" :key="item.value" :value="item.value" :label="item.label" />
          </NRadioGroup>
        </NFormItem>
        <NFormItem label="角色" path="roles">
          <NSelect v-model:value="model.roleId" :options="roleOptions" placeholder="请选择角色信息" />
        </NFormItem>
        <NFormItem label="群组" path="affiliation">
          <NTreeSelect
            v-model:value="model.affiliationId"
            :options="affiliationStore.affiliationTree"
            default-expand-all
            placeholder="请选择用户群组"
          />
        </NFormItem>
      </NForm>
      <template #footer>
        <NSpace :size="16">
          <NButton @click="closeDrawer">取消</NButton>
          <NButton type="primary" @click="handleSubmit">确认</NButton>
        </NSpace>
      </template>
    </NDrawerContent>
  </NDrawer>
</template>

<style scoped></style>
