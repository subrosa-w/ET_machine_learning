<template>
  <div>
    <h3 class="font-bold mb-2">Valores nulos por columna</h3>
    <div v-if="error" class="text-red-500">{{ error }}</div>
    <table v-if="Object.keys(nulls).length" class="table-auto w-full border text-xs">
      <thead>
        <tr>
          <th class="border px-2 py-1">Columna</th>
          <th class="border px-2 py-1">Nulos</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(val, col) in nulls" :key="col">
          <td class="border px-2 py-1">{{ col }}</td>
          <td class="border px-2 py-1">{{ val }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else>Cargando...</div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
const nulls = ref({})
const error = ref('')
onMounted(async () => {
  try {
    const res = await fetch('http://localhost:8000/api/nulls')
    const data = await res.json()
    if (res.ok) {
      nulls.value = data
    } else {
      error.value = data.error || 'Error al cargar nulos'
    }
  } catch (e) {
    error.value = 'No se pudo conectar al backend'
  }
})
</script> 