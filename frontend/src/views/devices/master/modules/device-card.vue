<script setup lang="ts">
import { computed } from "vue"
interface Props {
  status: "Offline" | "Online" | "Working" | "Danger"
  processCount?: number
  deviceName?: string
  permissionName?: string
  deviceDesc?: string
  platform?: string
}

const statusColor = {
  Offline: {
    color: "#909399",
    borderColor: ""
  },
  Online: {
    color: "#409EFF",
    borderColor: ""
  },
  Working: {
    color: "#E6A23C",
    borderColor: ""
  },
  Danger: {
    color: "#F56C6C",
    borderColor: "#F6CED7"
  }
}

const statusText = {
  Offline: "离线",
  Online: "在线",
  Working: "工作中",
  Danger: "错误"
}

const statusIcon = {
  Offline: "nrk:offline",
  Online: "mingcute:lightning-fill",
  Working: "eos-icons:hourglass",
  Danger: "bx:bxs-error"
}

const props = defineProps<Props>()

const boxStyle = computed(() => ({
  "--box-color": statusColor[props.status].color,
  "border-color": statusColor[props.status]?.borderColor,
  animation: props.status === "Danger" ? "" : "none"
}))
</script>

<template>
  <div>
    <div
      class="box-card w-300px sm:flex-1-hidden border-2 card-wrapper border-solid p-4 hover:border-primary"
      :style="boxStyle"
    >
      <div class="header h-40px flex items-center text-lg font-bold">
        <div>Mac OS</div>
        <NDivider vertical />
        <div class="flex items-center justify-center">
          <SvgIcon
            :icon="statusIcon[props.status]"
            class="text-20px"
            :style="{ color: statusColor[props.status].color }"
          />
          <div class="status ml-5px text-gray">{{ statusText[props.status] }}</div>
        </div>
      </div>
      <div class="content h-115px text-lg font-bold">
        <div>内容区域1231231231231</div>
      </div>
      <div class="footer h-50px flex items-center justify-between">
        <div
          class="processesNumber h-35px w-35px flex select-none items-center justify-center border border-primary rounded-full border-solid bg-green text-lg text-light font-bold"
        >
          4
        </div>
        <div class="title ml-5px w-65%">
          <div class="name text-14px font-bold">设备1</div>
          <div class="text-12px text-gray">超级管理员</div>
        </div>
        <div class="pushButton h-40px w-40px flex cursor-pointer items-center justify-center rounded-full bg-primary">
          <SvgIcon icon="material-symbols:chevron-right" class="text-28px color-light" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.box-card {
  position: relative;
  --box-color: #409eff;
  animation: flash 1.5s infinite;
}

@keyframes flash {
  0% {
    box-shadow: 0 0 10px rgba(245, 108, 108, 0.8);
  }
  50% {
    box-shadow: 0 0 20px rgba(245, 108, 108);
  }
  100% {
    box-shadow: 0 0 10px rgba(245, 108, 108, 0.8);
  }
}

.box-card::after {
  z-index: 2;
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 8px;
  background-color: var(--box-color);
}
</style>
