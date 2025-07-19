<template>
  <div class="bg-white rounded shadow p-4 mb-6">
    <h2 class="text-lg font-bold mb-2" style="color: #000">Regresión: Dinero gastado vs Probabilidad de ganar</h2>
    <div v-if="img">
      <img :src="img" alt="Gráfico de regresión dinero-probabilidad" class="mb-2" />
    </div>
    <div v-if="coef !== null && intercept !== null" class="text-xs" style="color: #000">
      <p style="color: #000"><b>Coeficiente (pendiente):</b> {{ coef.toExponential(2) }}</p>
      <p style="color: #000"><b>Intercepto:</b> {{ intercept.toFixed(4) }}</p>
    </div>
    <p v-else style="color: #000">Cargando regresión...</p>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
const img = ref('')
const coef = ref(null)
const intercept = ref(null)
onMounted(async () => {
  const res = await fetch('http://localhost:8000/api/regresion_dinero')
  const data = await res.json()
  img.value = data.img
  coef.value = data.coef
  intercept.value = data.intercept
})
</script> 