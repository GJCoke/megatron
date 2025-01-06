<script setup lang="ts">
import { enableStatusOptions } from "@/constants/business"
import { translateOptions } from "@/utils/common"
import { useAffiliationStore } from "@/store/modules/affiliation"

defineOptions({
  name: "UserSearch"
})

interface Emits {
  (e: "reset"): void
  (e: "search"): void
}

const emit = defineEmits<Emits>()

const model = defineModel<SystemManage.UserSearchParams>("model", { required: true })

const affiliationStore = useAffiliationStore()

async function reset() {
  emit("reset")
}

async function search() {
  emit("search")
}
</script>

<template>
  <NCard :bordered="false" size="small" class="card-wrapper">
    <NCollapse :default-expanded-names="['user-search']">
      <NCollapseItem title="搜索" name="user-search">
        <NForm :model="model" label-placement="left" :label-width="80">
          <NGrid responsive="screen" item-responsive>
            <NFormItemGi span="24 s:12 m:6" label="关键字" path="keyword" class="pr-24px">
              <NInput v-model:value="model.keyword" placeholder="输入关键字查询" />
            </NFormItemGi>
            <NFormItemGi span="24 s:12 m:7" label="用户群组" path="affiliationId" class="pr-24px">
              <NTreeSelect
                v-model:value="model.affiliationId"
                :options="affiliationStore.affiliationTree"
                default-expand-all
                placeholder="请选择用户群组"
                clearable
              />
            </NFormItemGi>
            <NFormItemGi span="24 s:12 m:6" label="用户状态" path="status" class="pr-24px">
              <NSelect
                v-model:value="model.status"
                placeholder="请选择用户状态"
                :options="translateOptions(enableStatusOptions)"
                clearable
              />
            </NFormItemGi>
            <NFormItemGi span="24 m:12 m:5" class="pr-24px">
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
      </NCollapseItem>
    </NCollapse>
  </NCard>
</template>

<style scoped></style>
