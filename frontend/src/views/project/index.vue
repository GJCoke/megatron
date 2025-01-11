<script setup lang="ts">
import { computed, reactive, ref } from "vue"
import { throttle } from "lodash-es"
import { fetchGetProjectList } from "@/service/api/project"
import ProjectOperateCard from "./modules/project-operate-card.vue"
import ProjectHeaderOperation from "./modules/project-header-operation.vue"

const searchParams = reactive({
  keyword: "",
  page: 1,
  pageSize: 20,
  total: 0
})

const projectList = ref<SystemProject.Project[]>([])
const loading = ref<boolean>(false)
const noMore = computed(() => {
  return searchParams.total <= projectList.value.length
})

/** 获取项目列表 */
async function getProjectList() {
  loading.value = true

  const { page, pageSize } = searchParams
  const { data, error } = await fetchGetProjectList({ page, pageSize, keyword: searchParams.keyword })

  if (!error) {
    projectList.value = [...projectList.value, ...data.records]
    searchParams.total = data.total
  }

  loading.value = false
}

/** 加载项目信息 */
function loadProjects() {
  if (loading.value || noMore.value) return

  if (!noMore.value) {
    searchParams.page += 1
    getProjectList()
  }
}

/** 添加节流, 防止频繁触发导致内容错乱 */
const handleLoad = throttle(loadProjects, 500)

getProjectList()
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <ProjectHeaderOperation v-model:model="searchParams" />
    <div class="sm:flex-1-hidden card-wrapper bg-card-box">
      <div class="h-full">
        <NInfiniteScroll v-if="projectList.length" class="p-16px" :distance="10" @load="handleLoad">
          <div class="flex flex-wrap gap-4">
            <div v-for="item in projectList" :key="item.id">
              <ProjectOperateCard
                :name="item.name"
                :driver-type="item.driverType"
                :describe="item.describe"
                :create-time="item.createTime"
                :users="item.users"
              />
            </div>
          </div>
          <div class="mt-16px font-bold">
            <div v-if="loading" class="flex items-center justify-center gap-2">
              <SvgIcon icon="eos-icons:bubble-loading" />
              <span class="text-base-text">加载中...</span>
            </div>
            <div v-if="noMore" class="text-center text-base-text">没有更多了...</div>
          </div>
        </NInfiniteScroll>
        <NEmpty v-else class="h-400px flex items-center justify-center" description="暂无项目">
          <template #extra>
            <NButton size="small">添加项目</NButton>
          </template>
        </NEmpty>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
