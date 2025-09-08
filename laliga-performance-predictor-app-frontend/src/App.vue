<template>
  <header class="bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-400 py-6 mb-8 shadow-lg rounded-b-xl">
    <div class="flex flex-col items-center">
      <h1 class="text-3xl md:text-4xl font-extrabold text-white tracking-wide drop-shadow">La Liga Performance Predictor</h1>
      <p class="text-white/80 mt-2 text-center">How are your players going to perform on future matches?</p>
    </div>
  </header>

  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-cyan-50 to-blue-100 text-gray-900 font-sans p-4">
    <div class="max-w-xl mx-auto mb-8">
      <SearchBar @player-selected="handlePlayerSelected" />
    </div>
    <div
      v-if="playerData && Object.keys(playerData).length > 0 && playerData.name && playerData.position && playerData.photo_url"
      class="mt-8 flex flex-col md:flex-row gap-8 items-stretch justify-center"
    >
      <div class="w-96 h-155">
        <PlayerCard :player="playerData" class="h-full" />
      </div>
      <div class="flex-1 w-full h-155">
       <PlayerDataTable
        :player="playerData"
        :stats="playerStats"
        :lastMatch="playerLastMatch"
        :performanceHistory="performanceHistory"
        class="h-full"
        />
      </div>
    </div>

    <div class="max-w-6xl mx-auto mt-6">
      <div class="flex flex-col md:flex-row gap-6 justify-center items-start">
        <div
          v-if="chartMatches.length"
          class="bg-white rounded-2xl shadow-lg p-6 w-full mb-4"
        >
          <PlayerCharts
            :matches="chartMatches"
            :extra-label="'Performance Rating'"
            :position="playerData?.position"
            chart-type="performance-history"
          />
        </div>
        <div
          v-if="chartMatches.length"
          class="bg-white rounded-2xl shadow-lg p-6 w-full mb-4"
        >
          <PlayerCharts
            :matches="chartMatches"
            :extra-label="getExtraLabel(playerData?.position)"
            :position="playerData?.position"
            chart-type="extra-history"
          />
        </div>
      </div>
    </div>

    <div class="mt-6 flex justify-center">
      <button
        v-if="playerData"
        @click="fetchPrediction"
        class="bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-semibold px-6 py-2 rounded-full shadow hover:scale-105 hover:from-blue-600 hover:to-cyan-600 transition-all"
        :disabled="loadingPrediction"
      >
        {{ loadingPrediction ? 'Predicting...' : 'Predict Performance' }}
      </button>
    </div>    

    <Suspense>
      <template #default>
        <div>
          <Predictions
            v-if="prediction"
            :prediction="prediction"
            :extra-label="getExtraLabel(playerData?.position)"
          />
          <div v-if="prediction">
            <div class="max-w-6xl mx-auto mt-6">
              <div class="flex flex-col md:flex-row gap-6 justify-center items-start">
                <div
                  v-if="perfChartMatches.length && !allPredPerfZero"
                  class="bg-white rounded-2xl shadow-lg p-6 w-full mb-4"
                >
                  <PlayerCharts
                    :matches="perfChartMatches"
                    :extra-label="'Performance Rating'"
                    :position="playerData?.position"
                    chart-type="performance-prediction"
                  />
                </div>
                <div
                  v-else-if="perfChartMatches.length && allPredPerfZero"
                  class="bg-white rounded-2xl shadow-lg p-6 w-full mb-4 flex items-center justify-center h-48"
                >
                  <span class="text-gray-500 text-lg">Not enough data available.</span>
                </div>
                <div
                  v-if="extraChartMatches.length && !allPredExtraZero"
                  class="bg-white rounded-2xl shadow-lg p-6 w-full mb-4"
                >
                  <PlayerCharts
                    :matches="extraChartMatches"
                    :extra-label="getExtraLabel(playerData?.position)"
                    :position="playerData?.position"
                    chart-type="extra-prediction"
                  />
                </div>
                <div
                  v-else-if="extraChartMatches.length && allPredExtraZero"
                  class="bg-white rounded-2xl shadow-lg p-6 w-full mb-4 flex items-center justify-center h-48"
                >
                  <span class="text-gray-500 text-lg">Not enough data available.</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
      <template #fallback>
        <div class="text-center mt-4 text-gray-500">Loading prediction...</div>
      </template>
    </Suspense>

    <footer class="mt-12 py-4 text-center text-gray-400 text-sm">
      © 2025 LaLiga Performance Predictor · All data is provided by FutbolFantasy website.
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import axios from 'axios'

import SearchBar from './components/SearchBar.vue'
import PlayerCard from './components/PlayerCard.vue'
import PlayerDataTable from './components/PlayerDataTable.vue'
import Predictions from './components/Predictions.vue'
import PlayerCharts from './components/PlayerCharts.vue'

const playerData = ref(null)
const playerStats = ref(null)
const playerLastMatch = ref(null)
const prediction = ref(null)
const loadingPrediction = ref(false)
const showEvolution = ref(false)
const showEvolutionCharts = ref(false)
const performanceHistory = ref([])

async function handlePlayerSelected(slug: string) {
  prediction.value = null
  showEvolution.value = false
  showEvolutionCharts.value = false
  performanceHistory.value = []
  try {
    const [infoRes, statsRes, lastMatchRes] = await Promise.all([
      axios.get(`http://localhost:8000/scraper/player-info/?player=${slug}`),
      axios.get(`http://localhost:8000/scraper/api/player-season-stats/?player=${slug}`),
      axios.get(`http://localhost:8000/scraper/api/player-last-match-stats/?player=${slug}`)
    ])
    playerData.value = infoRes.data
    playerStats.value = statsRes.data
    playerLastMatch.value = lastMatchRes.data 
    const perfRes = await axios.get(`http://localhost:8000/scraper/api/player-performance-evolution/?player=${slug}`)
    performanceHistory.value = perfRes.data
  } catch (error) {
    playerData.value = null
    playerStats.value = null
    playerLastMatch.value = null
    performanceHistory.value = []
  }
}

async function fetchPrediction() {
  if (!playerData.value?.slug) return
  loadingPrediction.value = true
  prediction.value = null
  showEvolution.value = false
  showEvolutionCharts.value = false
  try {
    const res = await axios.get(`http://localhost:8000/scraper/api/predict-performance/?player=${playerData.value.slug}`)
    prediction.value = res.data
    showEvolution.value = true
  } catch (e) {
    prediction.value = null
    alert('Prediction failed')
  } finally {
    loadingPrediction.value = false
  }
}

const chartMatches = computed(() =>
  (performanceHistory.value || []).map(m => ({
    matchDay: m.matchday,
    rating: m.performance_rating,
    extra: m.extra
  }))
)

function getExtraLabel(position?: string) {
  switch (position) {
    case 'POR':
    case 'goalkeeper':
      return 'Saves'
    case 'DEF':
    case 'defender':
      return 'Recoveries'
    case 'MED':
    case 'midfielder':
      return 'Key Passes'
    case 'DEL':
    case 'forward':
      return 'Goals'
    default:
      return 'Extra'
  }
}

const last5Matches = computed(() => (chartMatches.value || []).slice(-5))

const predictedPerformance = computed(() => {
  const windows = prediction.value?.windows || []
  const arr = prediction.value?.performance || []
  const indices = windows.map(w => parseInt(w.replace('next_', '')))
  const maxIndex = Math.max(...indices, 0)
  return Array.from({ length: maxIndex }, (_, idx) => {
    const valueIdx = indices.indexOf(idx + 1)
    return valueIdx !== -1
      ? {
          matchDay: `F${idx + 1}`,
          rating: arr[valueIdx],
          isPrediction: true,
          futureIndex: idx + 1
        }
      : {
          matchDay: `F${idx + 1}`,
          rating: null,
          isPrediction: true,
          futureIndex: idx + 1
        }
  })
})

const predictedExtra = computed(() => {
  const windows = prediction.value?.windows || []
  const arr = prediction.value?.extra || []
  const indices = windows.map(w => parseInt(w.replace('next_', '')))
  const maxIndex = Math.max(...indices, 0)
  return Array.from({ length: maxIndex }, (_, idx) => {
    const valueIdx = indices.indexOf(idx + 1)
    return valueIdx !== -1
      ? {
          matchDay: `F${idx + 1}`,
          extra: arr[valueIdx],
          isPrediction: true,
          futureIndex: idx + 1
        }
      : {
          matchDay: `F${idx + 1}`,
          extra: null,
          isPrediction: true,
          futureIndex: idx + 1
        }
  })
})

const perfChartMatches = computed(() => [
  ...last5Matches.value.map(m => ({
    matchDay: m.matchDay,
    rating: m.rating,
    isPrediction: false
  })),
  ...predictedPerformance.value
])

const extraChartMatches = computed(() => [
  ...last5Matches.value.map(m => ({
    matchDay: m.matchDay,
    extra: m.extra,
    isPrediction: false
  })),
  ...predictedExtra.value
])


const allPredPerfZero = computed(() => {
  const preds = predictedPerformance.value.map(p => p.rating)
  return preds.length > 0 ? preds.every(val => val === 0 || val == null) : true
})

const allPredExtraZero = computed(() => {
  const preds = predictedExtra.value.map(p => p.extra)
  return preds.length > 0 ? preds.every(val => val === 0 || val == null) : true
})

</script>