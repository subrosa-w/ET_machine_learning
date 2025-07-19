<template>
  <div>
    <label class="block font-bold mb-1">Selecciona columna numérica:</label>
    <select v-model="selected" @change="emitColumn" class="border px-2 py-1 rounded">
      <option v-for="col in columns" :key="col" :value="col">{{ col }}</option>
    </select>
    <div v-if="error" class="text-red-500">{{ error }}</div>
  </div>
</template>
<script setup>
import { ref, onMounted, defineEmits } from 'vue'
const columns = ref([])
const selected = ref('')
const error = ref('')
const emit = defineEmits(['update:column'])
const emitColumn = () => {
  emit('update:column', selected.value)
}
onMounted(async () => {
  try {
    const res = await fetch('http://localhost:8000/api/columns')
    const data = await res.json()
    if (res.ok) {
      columns.value = data
      selected.value = data[0] || ''
      emitColumn()
    } else {
      error.value = data.error || 'Error al cargar columnas'
    }
  } catch (e) {
    error.value = 'No se pudo conectar al backend'
  }
})
</script> 