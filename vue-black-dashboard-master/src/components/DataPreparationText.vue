<template>
  <div class="bg-white rounded shadow p-4 mb-6">
    <h2 class="text-lg font-bold mb-2" style="color: #000">FASE 3: Data Preparation</h2>
    <p v-if="text" style="color: #000">{{ text }}</p>
    <p v-else style="color: #000">Cargando resumen de preparación de datos...</p>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
const text = ref('')
onMounted(async () => {
  const res = await fetch('http://localhost:8000/api/data_preparation_text')
  const data = await res.json()
  text.value = data.text
})
</script> 