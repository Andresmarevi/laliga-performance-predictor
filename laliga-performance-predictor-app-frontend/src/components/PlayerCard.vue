<template>
  <div class="player-card p-6 bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-shadow max-w-xs mx-auto text-center h-full flex flex-col justify-center items-center">
    <img
      :src="player.photo_url"
      :alt="player.name"
      class="w-28 h-28 rounded-full object-cover mx-auto mb-4 border-4 border-blue-100 shadow"
    />
    <h2 class="text-2xl font-bold text-blue-700">{{ player.name }}</h2>
    <p class="text-gray-500 mt-1 italic">{{ positionFullName }}</p>
    <div v-if="player.team" class="flex items-center justify-center mt-3 gap-2">
      <img
        v-if="player.team_logo"
        :src="player.team_logo"
        :alt="player.team"
        class="inline-block h-8"
      />
      <span class="text-gray-700 font-medium">{{ player.team }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  player: {
    name: string
    position: string
    photo_url: string
    team?: string
    team_logo?: string
  }
}>()

const positionFullName = computed(() => {
  const pos = (props.player.position || '').toLowerCase()
  if (pos.includes('por')) return 'Goalkeeper'
  if (pos.includes('def')) return 'Defender'
  if (pos.includes('med')) return 'Midfielder'
  if (pos.includes('del')) return 'Forward'
  return props.player.position
})
</script>