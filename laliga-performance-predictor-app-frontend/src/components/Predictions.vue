<template>
  <div v-if="prediction" class="mt-4 flex justify-center">
    <div class="bg-white rounded-2xl shadow-lg p-6 w-full max-w-2xl">
      <h3 class="font-bold mb-4 text-center text-blue-700 text-xl">Prediction</h3>
      <div v-if="allRatingsZero" class="text-center text-gray-600 py-8">
        Not enough data available.
      </div>
      <template v-else>
        <table class="min-w-full text-sm border mx-auto rounded-xl overflow-hidden shadow">
          <thead class="bg-blue-50">
            <tr>
              <th class="border px-2 py-1">Window</th>
              <th class="border px-2 py-1">Performance Rating</th>
              <th class="border px-2 py-1">{{ extraLabel || 'Extra' }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(window, idx) in prediction.windows" :key="window" class="hover:bg-blue-50 transition">
              <td class="border px-2 py-1">{{ windowLabels[window] || window }}</td>
              <td class="border px-2 py-1">{{ scaledPerformance[idx] }}</td>
              <td class="border px-2 py-1">{{ prediction.extra[idx] }}</td>
            </tr>
          </tbody>
        </table>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  prediction: {
    windows: string[],
    performance: number[],
    extra: number[]
  },
  extraLabel?: string
}>()

const windowLabels: Record<string, string> = {
  next_1: 'Next match',
  next_2: 'Next 2 matches (average)',
  next_3: 'Next 3 matches (average)',
  next_5: 'Next 5 matches (average)',
}

const allRatingsZero = computed(() => {
  const perf = props.prediction?.performance
  return Array.isArray(perf) && perf.length > 0
    ? perf.every(val => val === 0)
    : true
})

function scalePerformanceLog(perf: number, position: string) {
  let max = 2
  const pos = (position || '').toLowerCase()
  if (pos.includes('med')) max = 3.5
  else if (pos.includes('def')) max = 1.8
  else if (pos.includes('del') || pos.includes('fw')) max = 1.2

  const factor = 10 / Math.log(1 + max)
  let scaled = factor * Math.log(1 + perf)
  if (scaled > 10) scaled = 10
  return Math.round(scaled * 100) / 100
}

const scaledPerformance = computed(() => {
  return (props.prediction.performance || []).map(perf => scalePerformanceLog(perf, ''))
})
</script>