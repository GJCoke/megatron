<script setup lang="ts">
import { computed } from "vue"

defineOptions({
  name: "UserCommonAvatar"
})

interface Props {
  username?: string
  src?: string | null
  size?: string | number
  slice?: number
  color?: string
}

const props = withDefaults(defineProps<Props>(), {
  slice: -3
})

/** 处理名称超过 `slice的正数` 时处理为最后的 `slice` 个字 */
const displayUsername = computed(() => {
  if (props.username && props.username.length > Math.abs(props.slice)) {
    return props.username.slice(props.slice)
  }
  return props.username
})

/** 获取一个随机的背景颜色 */
const randomColor = computed(() => {
  const color = ["#3b66e8", "#2bcb9f", "#8f1fd9"]
  return color[Math.floor(Math.random() * color.length)]
})
</script>

<template>
  <div>
    <NAvatar v-if="src" round :src="src" :size="size" />
    <NAvatar v-else round :color="color || randomColor" :size="size">
      <div class="p-2">{{ displayUsername }}</div>
    </NAvatar>
  </div>
</template>

<style scoped></style>
