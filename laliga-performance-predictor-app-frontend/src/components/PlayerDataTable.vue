<template>
  <div v-if="player && stats" class="bg-white rounded-2xl shadow-lg p-6">
    <h3 class="text-lg font-bold mb-4 text-blue-700">La Liga 2024-25 Stats</h3>
    <table class="min-w-full text-left">
      <tbody>
        <tr v-for="row in statRows" :key="row.label" class="hover:bg-blue-50 transition">
          <th class="pr-4 py-2 text-gray-600 font-medium">{{ row.label }}</th>
          <td class="py-2">{{ row.value ?? '-' }}</td>
        </tr>
        <tr v-for="row in lastMatchRows" :key="row.label" class="hover:bg-blue-50 transition">
          <th class="pr-4 py-2 text-gray-600 font-medium">{{ row.label }}</th>
          <td class="py-2">{{ row.value ?? '-' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  player: any,
  stats: any,
  lastMatch?: any,
  performanceHistory?: Array<{ matchday: number, performance_rating: number, extra: number }>
}>()

const statRows = computed(() => {
  const pos = (props.player?.position || '').toLowerCase()
  if (pos.includes('del')) {
    return [
      { label: 'Matches played (total minutes)', value: props.stats?.matches_played_display },
      { label: 'Goals', value: props.stats?.goals },
      { label: 'Assists', value: props.stats?.assists },
      { label: 'Shots on goal', value: props.stats?.shots_on_goal },
      { label: 'Dribbles', value: props.stats?.dribbles },
    ]
  } else if (pos.includes('med')) {
    return [
      { label: 'Matches played (total minutes)', value: props.stats?.matches_played_display },
      { label: 'Goals', value: props.stats?.goals },
      { label: 'Assists', value: props.stats?.assists },
      { label: 'Key passes', value: props.stats?.key_passes },
      { label: 'Recoveries', value: props.stats?.recoveries },
    ]
  } else if (pos.includes('def')) {
    return [
      { label: 'Matches played (total minutes)', value: props.stats?.matches_played_display },
      { label: 'Goals', value: props.stats?.goals },
      { label: 'Assists', value: props.stats?.assists },
      { label: 'Recoveries', value: props.stats?.recoveries },
      { label: 'Goals conceded', value: props.stats?.goals_conceded },
    ]
  } else if (pos.includes('por') || pos.includes('gk')) {
    return [
      { label: 'Matches played (total minutes)', value: props.stats?.matches_played_display },
      { label: 'Saves', value: props.stats?.saves },
      { label: 'Goal errors', value: props.stats?.goal_errors },
      { label: 'Penalties saved', value: props.stats?.penalties_saved },
      { label: 'Goals conceded', value: props.stats?.goals_conceded },
    ]
  }
  return [
    { label: 'Matches played (total minutes)', value: props.stats?.matches_played_display },
    { label: 'Goals', value: props.stats?.goals },
    { label: 'Assists', value: props.stats?.assists },
  ]
})

const lastMatchRows = computed(() => {
  const history = props.performanceHistory
  if (!history || !history.length) return []


  const ratings = history
    .map(m => m.performance_rating)
    .filter(r => typeof r === 'number' && !isNaN(r))

  if (!ratings.length) return []

  const pos = (props.player?.position || '').toLowerCase()
  let max = 2
  if (pos.includes('med')) max = 3.5
  else if (pos.includes('def')) max = 1.8
  else if (pos.includes('del') || pos.includes('fw')) max = 1.5

  function scalePerformanceLog(perf, max = 1.5) {
    const factor = 10 / Math.log(1 + max)
    let scaled = factor * Math.log(1 + perf)
    if (scaled > 10) scaled = 10
    return Math.round(scaled * 100) / 100
  }

  const avg = ratings.reduce((a, b) => a + b, 0) / ratings.length
  const scaled = scalePerformanceLog(avg, max)

  return [
    { label: 'Average performance rating', value: scaled }
  ]
})

</script>