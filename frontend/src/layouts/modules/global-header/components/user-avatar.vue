<script setup lang="ts">
import { computed } from "vue"
import type { VNode } from "vue"
import { useAuthStore } from "@/store/modules/auth"
import { useRouterPush } from "@/hooks/common/router"
import { useSvgIcon } from "@/hooks/common/icon"
import UserCommonAvatar from "@/components/common/user-common-avatar.vue"

defineOptions({
  name: "UserAvatar"
})

const authStore = useAuthStore()
const { routerPushByKey, toLogin } = useRouterPush()
const { SvgIconVNode } = useSvgIcon()

function loginOrRegister() {
  toLogin()
}

type DropdownKey = "logout"

type DropdownOption =
  | {
      key: DropdownKey
      label: string
      icon?: () => VNode
    }
  | {
      type: "divider"
      key: string
    }

const options = computed(() => {
  const opts: DropdownOption[] = [
    {
      label: "退出登录",
      key: "logout",
      icon: SvgIconVNode({ icon: "ph:sign-out", fontSize: 18 })
    }
  ]

  return opts
})

function logout() {
  window.$dialog?.info({
    title: "提示",
    content: "确认退出登录吗？",
    positiveText: "确认",
    negativeText: "取消",
    onPositiveClick: () => {
      authStore.resetStore()
    }
  })
}

function handleDropdown(key: DropdownKey) {
  if (key === "logout") {
    logout()
  } else {
    // If your other options are jumps from other routes, they will be directly supported here
    routerPushByKey(key)
  }
}
</script>

<template>
  <NButton v-if="!authStore.isLogin" quaternary @click="loginOrRegister">登录 / 注册</NButton>
  <NDropdown v-else placement="bottom" trigger="click" :options="options" @select="handleDropdown">
    <div>
      <ButtonIcon>
        <UserCommonAvatar :size="24" :username="authStore.userInfo.name" :src="authStore.userInfo.avatarUrl" />
        <span class="text-16px font-medium">{{ authStore.userInfo.name }}</span>
      </ButtonIcon>
    </div>
  </NDropdown>
</template>

<style scoped></style>
