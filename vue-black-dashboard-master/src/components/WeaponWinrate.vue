<template>
  <div class="bg-white rounded shadow p-4 mb-6">
    <h2 class="text-lg font-bold mb-2" style="color: #000">Tasa de victorias por tipo de arma</h2>
    <div v-if="img">
      <img :src="img" alt="Gráfico de tasa de victorias por arma" class="mb-2" />
    </div>
    <table v-if="table" class="table-auto w-full text-xs" style="color: #000">
      <thead>
        <tr>
          <th>Tipo de arma</th>
          <th>Tasa de victorias</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(valor, arma) in table" :key="arma">
          <td>{{ arma }}</td>
          <td>{{ (valor * 100).toFixed(2) }}%</td>
        </tr>
      </tbody>
    </table>
    <p v-else style="color: #000">Cargando datos de tasa de victorias...</p>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
const img = ref('')
const table = ref(null)
onMounted(async () => {
  const res = await fetch('http://localhost:8000/api/weapon_winrate')
  const data = await res.json()
  img.value = data.img
  table.value = data.table
})
</script> 