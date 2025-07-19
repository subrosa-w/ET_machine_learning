<template>
  <div>
    <h3 class="font-bold mb-2">Barplot</h3>
    <div v-if="error" class="text-red-500">{{ error }}</div>
    <div v-if="loading">Cargando barplot...</div>
    <img v-if="imgSrc" :src="imgSrc" alt="Barplot" class="max-w-full border rounded" />
  </div>
</template>
<script setup>
import { ref, watch, toRefs } from 'vue'
const props = defineProps({
  column: { type: String, required: true }
})
const { column } = toRefs(props)
const imgSrc = ref('')
const error = ref('')
const loading = ref(false)
async function fetchBarplot(col) {
  if (!col) return
  loading.value = true
  error.value = ''
  imgSrc.value = ''
  try {
    const res = await fetch(`http://localhost:8000/api/barplot?column=${encodeURIComponent(col)}`)
    const data = await res.json()
    if (res.ok && data.img) {
      imgSrc.value = data.img
    } else {
      error.value = data.error || 'No se pudo generar el barplot'
    }
  } catch (e) {
    error.value = 'No se pudo conectar al backend'
  }
  loading.value = false
}
watch(column, (newCol) => {
  fetchBarplot(newCol)
}, { immediate: true })
</script> 