<script setup lang="tsx">
import { computed, ref } from "vue"
import SvgIcon from "@/components/custom/svg-icon.vue"

defineOptions({
  name: "ProjectOperateCard"
})

type UserBriefInfo = SystemManage.UserBriefInfo & { color?: string }

interface Props {
  name: string
  driverType: string
  describe?: string | null
  createTime: string
  users: UserBriefInfo[]
}

const props = defineProps<Props>()

const UserAvatar = computed(() => {
  if (props.users.length > 5) {
    return [
      ...props.users.slice(-4),
      { name: `+${props.users.length - 4}`, avatarUrl: undefined, id: "rustAvatar", color: "gray" }
    ]
  }
  return props.users
})

const dropdownOptions = [
  {
    label: () => <span class="text-warning">编辑</span>,
    key: "edit",
    icon: () => <SvgIcon icon="material-symbols:edit-square-outline" class="text-16px color-warning" />
  },
  {
    label: () => <span class="text-error">删除</span>,
    key: "delete",
    icon: () => <SvgIcon icon="material-symbols:delete-outline-sharp" class="text-16px color-error" />
  }
]

const showDropdown = ref<boolean>(false)
const dropdownVisible = ref<boolean>(false)

/** 设置下拉框的展开状态 */
function setDropdownVisible(show: boolean) {
  dropdownVisible.value = show
}
</script>

<template>
  <div
    class="grid h-240px w-210px gap-2 border card-wrapper rd-16px border-solid bg-container p-4 hover:border-primary"
    @mouseover="showDropdown = true"
    @mouseleave="showDropdown = false"
  >
    <div class="mb-1 flex items-center justify-between text-lg text-base-text font-bold">
      <NEllipsis class="w-140px" :tooltip="false">{{ name }}</NEllipsis>
      <NDropdown
        v-if="showDropdown || dropdownVisible"
        trigger="click"
        :options="dropdownOptions"
        @update:show="setDropdownVisible"
      >
        <NButton quaternary circle size="small" type="primary">
          <SvgIcon icon="ic:outline-more-horiz" />
        </NButton>
      </NDropdown>
    </div>
    <div class="text-base-text">- {{ driverType }}</div>
    <NEllipsis class="h-60px text-base-text" :line-clamp="3" :tooltip="false">{{ describe }}</NEllipsis>
    <div class="h-40px flex gap-1">
      <div v-for="item in UserAvatar" :key="item.id">
        <UserCommonAvatar :username="item.name" :src="item.avatarUrl" :color="item.color" />
      </div>
    </div>
    <div class="text-12px text-gray">{{ createTime }}</div>
  </div>
</template>

<style scoped></style>
