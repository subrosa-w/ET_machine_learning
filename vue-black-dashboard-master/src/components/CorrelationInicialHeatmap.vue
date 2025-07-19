<template>
  <div class="bg-white rounded shadow p-4 mb-6">
    <h2 class="text-lg font-bold mb-2" style="color: #000">Correlación entre Variables Inicial</h2>
    <div v-if="img">
      <img :src="img" alt="Heatmap de correlación inicial" class="mb-2" />
    </div>
    <p v-else style="color: #000">Cargando heatmap de correlación inicial...</p>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
const img = ref('')
onMounted(async () => {
  const res = await fetch('http://localhost:8000/api/corr_inicial')
  const data = await res.json()
  img.value = data.img
})
</script> 