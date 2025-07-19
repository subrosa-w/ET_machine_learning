<template>
  <div>
    <h3 class="font-bold mb-2">Estadísticas descriptivas</h3>
    <div v-if="error" class="text-red-500">{{ error }}</div>
    <table v-if="rows.length" class="table-auto w-full border text-xs">
      <thead>
        <tr>
          <th class="border px-2 py-1">Estadística</th>
          <th v-for="col in columns" :key="col" class="border px-2 py-1">{{ col }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, i) in rows" :key="i">
          <td class="border px-2 py-1">{{ row.stat }}</td>
          <td v-for="col in columns" :key="col" class="border px-2 py-1">{{ row[col] }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else>Cargando...</div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
const rows = ref([])
const columns = ref([])
const error = ref('')
onMounted(async () => {
  try {
    const res = await fetch('http://localhost:8000/api/describe')
    const data = await res.json()
    if (res.ok) {
      columns.value = Object.keys(data)
      const stats = Object.keys(data[columns.value[0]] || {})
      rows.value = stats.map(stat => {
        const row = { stat }
        columns.value.forEach(col => { row[col] = data[col][stat] })
        return row
      })
    } else {
      error.value = data.error || 'Error al cargar estadísticas'
    }
  } catch (e) {
    error.value = 'No se pudo conectar al backend'
  }
})
</script> 