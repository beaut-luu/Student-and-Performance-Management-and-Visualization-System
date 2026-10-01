<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: { type: String, default: '' },
  size: { type: Number, default: 48 },
})

// 后端没有头像字段，这里用用户名首字符 + 由用户名派生的固定底色生成头像
const initial = computed(() => (props.name ? props.name.trim().charAt(0).toUpperCase() : '?'))

const avatarStyle = computed(() => {
  let hash = 0
  for (const ch of props.name || '?') hash = (hash * 31 + ch.codePointAt(0)) % 360
  return {
    width: `${props.size}px`,
    height: `${props.size}px`,
    fontSize: `${Math.round(props.size * 0.42)}px`,
    background: `hsl(${hash}, 62%, 52%)`,
  }
})
</script>

<template>
  <span class="avatar" :style="avatarStyle">{{ initial }}</span>
</template>

<style scoped>
.avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: #fff;
  font-weight: 600;
  user-select: none;
  flex: none;
}
</style>
