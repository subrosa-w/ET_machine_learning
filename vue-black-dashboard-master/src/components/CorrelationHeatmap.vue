<template>
  <div>
    <h3 class="font-bold mb-2">Heatmap de correlación</h3>
    <div v-if="error" class="text-red-500">{{ error }}</div>
    <div v-if="loading">Cargando heatmap...</div>
    <img v-if="imgSrc" :src="imgSrc" alt="Heatmap de correlación" class="max-w-full border rounded" />
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
const imgSrc = ref('')
const error = ref('')
const loading = ref(false)
onMounted(async () => {
  loading.value = true
  try {
    const res = await fetch('http://localhost:8000/api/corr')
    const data = await res.json()
    if (res.ok && data.img) {
      imgSrc.value = data.img
    } else {
      error.value = data.error || 'No se pudo generar el heatmap'
    }
  } catch (e) {
    error.value = 'No se pudo conectar al backend'
  }
  loading.value = false
})
</script> 