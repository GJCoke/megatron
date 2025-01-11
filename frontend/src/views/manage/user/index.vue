<script setup lang="ts">
import { ref } from "vue"
import type { GroupTree } from "@/store/modules/affiliation"
import UserSideOperation from "./modules/user-sider-operation.vue"
import UserContentOperation from "./modules/user-content-operation.vue"

const nodeId = ref<number | null>(null)

function userSideRowClick(node: GroupTree) {
  nodeId.value = node.key
}
</script>

<template>
  <div class="flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <div class="h-full flex gap-2">
      <UserSideOperation class="w-300px" @node-click="userSideRowClick" />
      <UserContentOperation class="flex-1" :node-id="nodeId" />
    </div>
  </div>
</template>

<style scoped></style>
