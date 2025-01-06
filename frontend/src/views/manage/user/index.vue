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
  <div class="min-h-500px flex-col-stretch overflow-hidden lt-sm:overflow-auto">
    <NLayout has-sider class="card-wrapper">
      <NLayoutSider
        :show-collapsed-content="false"
        show-trigger="bar"
        collapse-mode="transform"
        :collapsed-width="12"
        :native-scrollbar="false"
        bordered
        content-style="padding: 16px;"
      >
        <UserSideOperation @node-click="userSideRowClick" />
      </NLayoutSider>
      <NLayoutContent :native-scrollbar="false" content-style="padding: 20px;">
        <UserContentOperation :node-id="nodeId" />
      </NLayoutContent>
    </NLayout>
  </div>
</template>

<style scoped></style>
