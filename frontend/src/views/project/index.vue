<script setup lang="ts">
import { computed, reactive, ref } from "vue"
import { throttle } from "lodash-es"
import { useDialog } from "naive-ui"
import { deleteProjectInfo, fetchGetProjectList } from "@/service/api/project"
import { useBoolean, useLoading } from "~/packages/hooks"
import ProjectOperateCard from "./modules/project-operate-card.vue"
import ProjectHeaderOperation from "./modules/project-header-operation.vue"
import ProjectOperateModal from "./modules/project-operate-modal.vue"

const searchParams = reactive({
  keyword: "",
  page: 1,
  pageSize: 20,
  total: 0
})

const projectList = ref<SystemProject.Project[]>([])
const { loading, startLoading, endLoading } = useLoading()
const noMore = computed(() => {
  return searchParams.total <= projectList.value.length
})

const { bool: visible, setTrue: openModal } = useBoolean()
const operateType = ref<NaiveUI.TableOperateType>("add")

/** 获取项目列表 */
async function getProjectList() {
  startLoading()

  const { page, pageSize } = searchParams
  const { data, error } = await fetchGetProjectList({ page, pageSize, keyword: searchParams.keyword })

  if (!error) {
    projectList.value = [...projectList.value, ...data.records]
    searchParams.total = data.total
  }

  endLoading()
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

const editingData = ref<SystemProject.Project | null>(null)

function handleAdd() {
  operateType.value = "add"
  openModal()
}

function handleEdit(item: SystemProject.Project) {
  operateType.value = "edit"
  editingData.value = { ...item }
  openModal()
}

const dialog = useDialog()

/** 删除指定项目 */
async function handleDelete(id: number) {
  dialog.warning({
    title: "确认删除",
    content: "确认删除此项目吗？",
    positiveText: "确认",
    negativeText: "取消",
    negativeButtonProps: {
      size: "medium"
    },
    positiveButtonProps: {
      type: "primary",
      size: "medium"
    },
    onPositiveClick: async () => {
      const { error } = await deleteProjectInfo(id)

      if (!error) {
        const index = projectList.value.findIndex((item) => item.id === id)
        projectList.value.splice(index, 1)
        searchParams.total -= 1
      }
    }
  })
}

/** 假更新, 如不同人同时操作做时内容可能失真 */
function updateLocalProjectInfo(project: SystemProject.Project) {
  const index = projectList.value.findIndex((item) => item.id === project.id)
  if (index !== -1) {
    projectList.value[index] = project
  } else {
    searchParams.total += 1
    /** 如果已经加载完毕则在数组中添加一个, 否则不添加 */
    if (noMore.value) {
      projectList.value.push(project)
    }
  }
}

/** 查询 */
function searchProject() {
  searchParams.page = 1
  projectList.value = []
  getProjectList()
}

/** 重置 */
function resetProject() {
  searchParams.keyword = ""
  searchParams.page = 1
}

function goToProjectDetails(id: number) {
  console.log("projectId", id)
}

getProjectList()
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <ProjectHeaderOperation
      v-model:model="searchParams"
      :total="searchParams.total"
      @add="handleAdd"
      @search="searchProject"
      @reset="resetProject"
    />
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
                @edit="handleEdit(item)"
                @delete="handleDelete(item.id)"
                @click="goToProjectDetails(item.id)"
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
            <NButton size="small" @click="handleAdd">添加项目</NButton>
          </template>
        </NEmpty>
      </div>
    </div>
    <ProjectOperateModal
      v-model:visible="visible"
      :operate-type="operateType"
      :row-data="editingData"
      @submitted="updateLocalProjectInfo"
    />
  </div>
</template>

<style scoped></style>
