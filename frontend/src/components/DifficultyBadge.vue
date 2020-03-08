<template>
  <span v-bind:title="difficultyTitle">
    <span class="difficulty-badge" v-for="index in difficulty" :key="index">
      <span>🏆</span>
    </span>
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

<style scoped>
</style>
