<script setup lang="ts">
defineOptions({
  name: "ProjectHeaderOperation"
})

interface Emits {
  (e: "reset"): void
  (e: "search"): void
  (e: "add"): void
}

const emit = defineEmits<Emits>()

const model = defineModel<SystemManage.RoleSearchParams>("model", { required: true })

function reset() {
  emit("reset")
}

function search() {
  emit("search")
}

function add() {
  emit("add")
}
</script>

<template>
  <NCard :bordered="false" size="small" class="card-wrapper">
    <div class="h-50px flex items-center justify-between">
      <NForm :model="model">
        <NGrid responsive="screen" item-responsive>
          <NFormItemGi span="12 s:12 m:6" path="keyword" class="pr-24px">
            <NInput v-model:value="model.keyword" round placeholder="输入项目名称查询">
              <template #prefix>
                <SvgIcon icon="hugeicons:search-01" />
              </template>
            </NInput>
          </NFormItemGi>
          <NFormItemGi span="24 s:12 m:6">
            <NSpace class="w-full" justify="end">
              <NButton @click="reset">
                <template #icon>
                  <icon-ic-round-refresh class="text-icon" />
                </template>
                重置
              </NButton>
              <NButton type="primary" ghost @click="search">
                <template #icon>
                  <icon-ic-round-search class="text-icon" />
                </template>
                搜索
              </NButton>
            </NSpace>
          </NFormItemGi>
        </NGrid>
      </NForm>
      <div class="flex items-center gap-24px">
        <div>
          共
          <span class="text-lg text-primary font-bold">20</span>
          个项目
        </div>
        <NButton type="primary" @click="add">
          <template #icon>
            <icon-ic-round-plus class="text-icon" />
          </template>
          新增
        </NButton>
      </div>
    </div>
  </NCard>
</template>

<style scoped></style>
