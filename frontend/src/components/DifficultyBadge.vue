<template>
  <span v-bind:title="difficultyTitle">{{ currentDifficultyLevelEmoji }}</span>
</template>

<script>
export default {
  name: 'DifficultyBadge',
  props: {
    difficulty: [Number, String],
  },

  data() {
    return {
      difficultyTitle: `Difficulté ${this.difficulty}/4`,
    };
  },

  computed: {
    currentDifficultyLevelEmoji() {
      return this.$store.getters.getDifficultyLevelEmojiByValue(parseInt(this.difficulty, 10));
    },
  },
};
</script>
