<template>
  <div>
    <h3 class="font-bold mb-2">Resumen de datos</h3>
    <div v-if="error" class="text-red-500">{{ error }}</div>
    <table v-if="rows.length" class="table-auto w-full border">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col" class="border px-2 py-1">{{ col }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, i) in rows" :key="i">
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
    const res = await fetch('http://localhost:8000/api/summary')
    const data = await res.json()
    if (res.ok) {
      rows.value = data
      columns.value = data.length ? Object.keys(data[0]) : []
    } else {
      error.value = data.error || 'Error al cargar resumen'
    }
  } catch (e) {
    error.value = 'No se pudo conectar al backend'
  }
})
</script> 