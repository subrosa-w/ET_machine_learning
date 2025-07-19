<template>
  <div>
    <h3 class="font-bold mb-2">Descripción del EDA</h3>
    <div v-if="error" class="text-red-500">{{ error }}</div>
    <div v-if="text" class="bg-gray-100 p-3 rounded border">{{ text }}</div>
    <div v-else>Cargando...</div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
const text = ref('')
const error = ref('')
onMounted(async () => {
  try {
    const res = await fetch('http://localhost:8000/api/eda_text')
    const data = await res.json()
    if (res.ok && data.text) {
      text.value = data.text
    } else {
      error.value = data.error || 'Error al cargar el texto del EDA'
    }
  } catch (e) {
    error.value = 'No se pudo conectar al backend'
  }
})
</script> 