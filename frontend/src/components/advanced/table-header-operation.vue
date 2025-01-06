<script setup lang="ts">
defineOptions({
  name: "TableHeaderOperation"
})

interface Props {
  itemAlign?: NaiveUI.Align
  disabledDelete?: boolean
  loading?: boolean
  canBatchDelete?: boolean
  canAdd?: boolean
}

withDefaults(defineProps<Props>(), {
  canBatchDelete: true,
  canAdd: true,
  itemAlign: undefined
})

interface Emits {
  (e: "add"): void
  (e: "delete"): void
  (e: "refresh"): void
}

const emit = defineEmits<Emits>()

function add() {
  emit("add")
}

function batchDelete() {
  emit("delete")
}

function refresh() {
  emit("refresh")
}
</script>

<template>
  <NSpace :align="itemAlign" wrap justify="end" class="lt-sm:w-200px">
    <slot name="prefix"></slot>
    <slot name="default">
      <NButton v-if="canAdd" size="small" ghost type="primary" @click="add">
        <template #icon>
          <icon-ic-round-plus class="text-icon" />
        </template>
        新增
      </NButton>
      <NPopconfirm v-if="canBatchDelete" @positive-click="batchDelete">
        <template #trigger>
          <NButton size="small" ghost type="error" :disabled="disabledDelete">
            <template #icon>
              <icon-ic-round-delete class="text-icon" />
            </template>
            批量删除
          </NButton>
        </template>
        确认删除吗？
      </NPopconfirm>
    </slot>
    <NButton size="small" @click="refresh">
      <template #icon>
        <icon-mdi-refresh class="text-icon" :class="{ 'animate-spin': loading }" />
      </template>
      刷新
    </NButton>
    <slot name="suffix"></slot>
  </NSpace>
</template>

<style scoped></style>
