<template>
  <div class="question-card">
    <!-- <div class="question-card__header"></div> -->
    <div class="question-card__content">
      <p>{{ question.text }}</p>
    </div>
    <div class="question-card__extra">
      <DifficultyBadge v-bind:difficulty="question.difficulty" />
    </div>
  </div>
</template>

<script>
import DifficultyBadge from './DifficultyBadge.vue'

export default {
  name: 'QuestionCard',
  props: {
    question: Object
  },
  components: {
    DifficultyBadge
  }
}
</script>

<style scoped>
.question-card {
  height: 100%;
}
.question-card__content {
  height: 50%;
  padding: 10px;
  overflow: hidden;
}
.question-card__content :last-child {
  margin-bottom: 0;
}
.question-card__extra {
  padding: 10px;
}
.category {
  text-align: right;
  display: inline-block;
  border: 1px solid #F33F3F;
  border-radius: 5px;
  margin: 5px;
  padding: 5px;
  cursor: pointer;
}
</style>