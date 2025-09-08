<template>
  <div class="max-w-xl mx-auto">
    <label for="player-search" class="block text-sm font-medium text-gray-700 mb-1">
      Search for a player
    </label>
    <div class="relative">
      <input
        id="player-search"
        v-model="query"
        @input="filterPlayers"
        placeholder="Type a player's name..."
        class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-full shadow focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
        autocomplete="off"
      />
      <svg class="absolute left-3 top-2.5 w-5 h-5 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
      </svg>
    </div>
    <ul v-if="filtered.length && query" class="mt-2 border rounded-lg bg-white shadow divide-y max-h-60 overflow-auto">
      <li
        v-for="player in filtered"
        :key="player.slug"
        @click="selectPlayer(player)"
        class="p-2 hover:bg-blue-100 cursor-pointer transition"
      >
        {{ player.name }}
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits(['player-selected'])

const query = ref('')
const filtered = ref<{name: string, slug: string}[]>([])

let controller: AbortController | null = null

async function filterPlayers() {
  const q = query.value.trim()
  if (q.length < 2) {
    filtered.value = []
    return
  }

  if (controller) controller.abort()
  controller = new AbortController()

  try {
    const res = await fetch(`/api/search-players/?q=${encodeURIComponent(q)}`, { signal: controller.signal })
    if (!res.ok) throw new Error('Error en búsqueda')
    const data = await res.json()
    filtered.value = data.results
  } catch (error) {
    if ((error as any).name !== 'AbortError') {
      console.error(error)
      filtered.value = []
    }
  }
}

function selectPlayer(player: {name: string, slug: string}) {
  emit('player-selected', player.slug)
  query.value = player.name
  filtered.value = []
}
</script>