<template>
  <span title="Difficulté">
    <span class="difficulty-badge" v-for="index in difficulty" :key="index">
      <span>🏆</span>
    </span>
  </span>
</template>

<script>
export default {
  name: 'DifficultyBadge',
  props: {
    difficulty: Number
  },
}
</script>

<style scoped>
</style>
