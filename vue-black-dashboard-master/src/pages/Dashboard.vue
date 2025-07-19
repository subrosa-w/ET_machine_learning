<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Dashboard EDA CS:GO (Resumen Esencial)</h1>
    <EDAText class="mb-6" />
    <DataPreparationText class="mb-6" />
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
      <div>
        <DataSummary />
        <DescribeTable class="mt-6" />
        <NullsTable class="mt-6" />
      </div>
      <div>
        <WeaponUsage />
        <WeaponWinrate class="mt-6" />
      </div>
    </div>
  </div>
</template>
<script setup>
import LineChart from "@/components/Charts/LineChart";
import BarChart from "@/components/Charts/BarChart";
import BaseTable from "@/components/BaseTable";
import * as chartConfigs from "@/components/Charts/config";
import Papa from "papaparse";
import config from "@/config";
import DataSummary from '../components/DataSummary.vue'
import ColumnSelector from '../components/ColumnSelector.vue'
import HistogramChart from '../components/HistogramChart.vue'
import DescribeTable from '../components/DescribeTable.vue'
import CorrelationHeatmap from '../components/CorrelationHeatmap.vue'
import NullsTable from '../components/NullsTable.vue'
import BarPlotChart from '../components/BarPlotChart.vue'
import BoxPlotChart from '../components/BoxPlotChart.vue'
import EDAText from '../components/EDAText.vue'
import DataPreparationText from '../components/DataPreparationText.vue'
import WeaponUsage from '../components/WeaponUsage.vue'
import WeaponWinrate from '../components/WeaponWinrate.vue'
import RegresionDinero from '../components/RegresionDinero.vue'
import CorrelationInicialHeatmap from '../components/CorrelationInicialHeatmap.vue'
import { ref, onMounted } from 'vue'
const selectedColumn = ref('')
const columns = ref([])

function mean(arr) {
  const nums = arr.filter(x => typeof x === 'number' && !isNaN(x));
  if (!nums.length) return null;
  return nums.reduce((a, b) => a + b, 0) / nums.length;
}
function median(arr) {
  const nums = arr.filter(x => typeof x === 'number' && !isNaN(x)).sort((a, b) => a - b);
  if (!nums.length) return null;
  const mid = Math.floor(nums.length / 2);
  return nums.length % 2 !== 0 ? nums[mid] : (nums[mid - 1] + nums[mid]) / 2;
}
function mode(arr) {
  const freq = {};
  let max = 0, res = null;
  arr.forEach(x => {
    if (x == null) return;
    freq[x] = (freq[x] || 0) + 1;
    if (freq[x] > max) {
      max = freq[x];
      res = x;
    }
  });
  return res;
}
function std(arr) {
  const m = mean(arr);
  const nums = arr.filter(x => typeof x === 'number' && !isNaN(x));
  if (!nums.length) return null;
  return Math.sqrt(nums.reduce((a, b) => a + Math.pow(b - m, 2), 0) / nums.length);
}

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:8000/api/columns')
    const data = await res.json()
    if (res.ok && data.length) {
      columns.value = data
      selectedColumn.value = data[0]
    }
  } catch (e) {
    // Si falla, no hacer nada
  }
})

</script>
<style></style>
