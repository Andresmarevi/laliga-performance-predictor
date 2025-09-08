<template>
  <div v-if="matches && matches.length" class="w-full bg-white shadow rounded-xl p-4 mb-6 md:mb-0">
    <h3 class="text-lg font-bold mb-2 text-center">
      <template v-if="chartType === 'performance-prediction'">
        Last 5 Games + Predicted Performance
      </template>
      <template v-else-if="chartType === 'extra-prediction'">
        Last 5 Games + Predicted {{ extraLabel || 'Extra' }}
      </template>
      <template v-else-if="chartType === 'performance-history'">
        Season Performance
      </template>
      <template v-else-if="chartType === 'extra-history'">
        Season {{ extraLabel || 'Extra' }}
      </template>
    </h3>
    <div
      v-if="chartType === 'performance-prediction' || chartType === 'extra-prediction'"
      class="flex flex-col items-center mb-2 text-sm text-gray-700"
    >
      <div class="flex flex-wrap gap-4 justify-center">
        <span class="flex items-center">
          <span
            class="inline-block w-4 h-4 rounded-full mr-1 border-2"
            :class="chartType === 'performance-prediction' ? 'border-blue-500 bg-blue-500' : 'border-orange-400 bg-orange-400'"
          ></span>
          Real data
        </span>
        <span class="flex items-center">
          <span class="inline-block w-4 h-4 rounded-full mr-1 border-2 border-red-500 bg-white border-4"></span>
          Predicted data
        </span>
      </div>
    </div>
    <Line
      v-if="chartType === 'performance-prediction' || chartType === 'performance-history'"
      :data="performanceData"
      :options="performanceOptions"
    />
    <Line
      v-else
      :data="extraData"
      :options="extraOptions"
    />
  </div>
</template>

<script setup lang="ts">
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Line } from 'vue-chartjs'
import { defineProps, computed } from 'vue'
import annotationPlugin from 'chartjs-plugin-annotation'

ChartJS.register(annotationPlugin)
ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale)

const props = defineProps<{
  matches: { matchDay: string | number; rating?: number; extra?: number; isPrediction?: boolean }[],
  extraLabel?: string,
  position?: string,
  chartType?: string
}>()

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

const splitIndex = computed(() => props.matches.findIndex(m => m.isPrediction))

const annotation = computed(() =>
  splitIndex.value > 0
    ? {
        plugins: {
          annotation: {
            annotations: {
              pastBox: {
                type: 'box',
                xMin: 0 - 0.5,
                xMax: splitIndex.value - 0.5,
                backgroundColor: 'rgba(59, 130, 246, 0.05)',
                borderWidth: 0,
              },
              futureBox: {
                type: 'box',
                xMin: splitIndex.value - 0.5,
                xMax: props.matches.length - 1 + 0.5,
                backgroundColor: 'rgba(255, 99, 132, 0.08)',
                borderWidth: 0,
              },
              splitLine: {
                type: 'line',
                xMin: splitIndex.value - 0.5,
                xMax: splitIndex.value - 0.5,
                borderColor: 'red',
                borderWidth: 2,
                label: {
                  content: 'Prediction',
                  enabled: true,
                  position: 'start',
                  color: 'red',
                  font: { weight: 'bold' }
                }
              }
            }
          }
        }
      }
    : {}
)

const performanceData = computed(() => {
  const data = props.matches.map((m) =>
    m.rating != null ? scalePerformanceLog(m.rating, props.position || '') : null
  )
  const movingAvg = movingAverage(data, 3)
  const pointBackgroundColors = props.matches.map(m =>
    m.isPrediction ? '#fff' : '#3b82f6'
  )
  const pointBorderColors = props.matches.map(m =>
    m.isPrediction ? '#FF0000' : '#3b82f6'
  )
  const pointRadius = props.matches.map(m =>
    m.isPrediction ? 8 : 4
  )
  const pointBorderWidth = props.matches.map(m =>
    m.isPrediction ? 4 : 2
  )
  const datasets = [
    {
      label: 'Performance Rating',
      data,
      borderColor: '#3b82f6',
      backgroundColor: '#3b82f680',
      fill: false,
      tension: 0.2,
      spanGaps: true,
      pointBackgroundColor: pointBackgroundColors,
      pointBorderColor: pointBorderColors,
      pointRadius: pointRadius,
      pointBorderWidth: pointBorderWidth,
    }
  ]
  if (props.chartType === 'performance-history') {
    datasets.push({
      label: 'Moving Average',
      data: movingAvg,
      borderColor: '#60a5fa',
      backgroundColor: 'transparent',
      fill: false,
      tension: 0.2,
      spanGaps: true,
      borderDash: [6, 6],
      pointRadius: 0,
      pointBorderWidth: 0,
    })
  }
  return {
    labels: props.matches.map((m) => m.matchDay),
    datasets
  }
})

const extraData = computed(() => {
  const data = props.matches.map((m) => m.extra)
  const movingAvg = movingAverage(data, 3)
  const pointBackgroundColors = props.matches.map(m =>
    m.isPrediction ? '#fff' : '#f59e42'
  )
  const pointBorderColors = props.matches.map(m =>
    m.isPrediction ? '#FF0000' : '#f59e42'
  )
  const pointRadius = props.matches.map(m =>
    m.isPrediction ? 8 : 4
  )
  const pointBorderWidth = props.matches.map(m =>
    m.isPrediction ? 4 : 2
  )
  const datasets = [
    {
      label: props.extraLabel || 'Extra',
      data,
      borderColor: '#f59e42',
      backgroundColor: '#f59e4280',
      fill: false,
      tension: 0.2,
      spanGaps: true,
      pointBackgroundColor: pointBackgroundColors,
      pointBorderColor: pointBorderColors,
      pointRadius: pointRadius,
      pointBorderWidth: pointBorderWidth,
    }
  ]
  if (props.chartType === 'extra-history') {
    datasets.push({
      label: 'Moving Average',
      data: movingAvg,
      borderColor: '#fbbf24',
      backgroundColor: 'transparent',
      fill: false,
      tension: 0.2,
      spanGaps: true,
      borderDash: [6, 6],
      pointRadius: 0,
      pointBorderWidth: 0,
    })
  }
  return {
    labels: props.matches.map((m) => m.matchDay),
    datasets
  }
})


const performanceOptions = computed(() => ({
  responsive: true,
  scales: {
    x: {
      title: { display: true, text: 'Match' }
    },
    y: {
      type: 'linear',
      position: 'left',
      suggestedMin: 0,
      suggestedMax: 10,
      title: { display: true, text: 'Performance Rating' }
    }
  },
  ...annotation.value
}))

const extraOptions = computed(() => ({
  responsive: true,
  scales: {
    x: {
      title: { display: true, text: 'Match' }
    },
    y: {
      type: 'linear',
      position: 'left',
      suggestedMin: 0,
      title: { display: true, text: props.extraLabel || 'Extra' }
    }
  },
  ...annotation.value
}))

function movingAverage(arr: (number | null)[], window: number): (number | null)[] {
  const result: (number | null)[] = []
  for (let i = 0; i < arr.length; i++) {
    let sum = 0
    let count = 0
    for (let j = i; j > i - window && j >= 0; j--) {
      if (arr[j] != null) {
        sum += arr[j] as number
        count++
      }
    }
    result.push(count === window ? Math.round((sum / window) * 100) / 100 : null)
  }
  return result
}

</script>