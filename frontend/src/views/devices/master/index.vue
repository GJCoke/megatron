<script setup lang="ts">
import DeviceCard from "./modules/device-card.vue"
</script>

<template>
  <div class="flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <NCard :bordered="false" size="small" class="sm:flex-1-hidden card-wrapper">
      <template #header>
        <div class="flex items-center gap-2">
          <div>设备列表</div>
          <NDivider vertical />
          <NButton type="primary" size="small">
            <template #icon>
              <SvgIcon icon="material-symbols:add" />
            </template>
            添加设备
          </NButton>
        </div>
      </template>
      <template #header-extra>
        <div>
          共
          <span class="text-lg text-primary font-bold">20</span>
          个设备
        </div>
      </template>
      <div class="flex items-center gap-2 mt-2 mb-6">
        <div class="w-300px">
          <NInput round placeholder="输入设备名称查询">
            <template #prefix>
              <SvgIcon icon="hugeicons:search-01" />
            </template>
          </NInput>
        </div>
        <div>112233</div>
      </div>
      <div class="flex gap-4">
        <DeviceCard status="Working" />
        <DeviceCard status="Online" />
        <DeviceCard status="Danger" />
        <DeviceCard status="Offline" />
      </div>
    </NCard>
  </div>
</template>

<style scoped>

</style>
