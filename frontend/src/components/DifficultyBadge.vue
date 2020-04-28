<template>
  <span v-bind:title="difficultyTitle">
    <template v-if="difficulty === 0">🧸</template>
    <template v-if="difficulty != 0">
      <span class="difficulty-badge" v-for="index in difficulty" :key="index">
        <span>🏆</span>
      </span>
    </template>
  </span>
</template>

<script>
export default {
  name: 'DifficultyBadge',
  props: {
    difficulty: Number,
  },

  data() {
    return {
      difficultyTitle: `Difficulté ${this.difficulty}/4`,
    }
  },
}
</script>
