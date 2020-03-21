<template>
  <div class="question-card">
    <!-- <div class="question-card__header"></div> -->
    <div class="question-card__content">
      <p>{{ question.text }}</p>
    </div>
    <hr class="question-card__seperator">
    <div class="question-card__extra">
      <span class="color-orange">{{ question.category }}</span>
      <DifficultyBadge class="question-card__extra__badge" v-bind:difficulty="question.difficulty" />
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
.question-card__seperator {
  border: 0 none;
  height: 1px;
  width: 50%;
  color: #005995;
  background-color: #005995;
}
.question-card__extra {
  text-align: left;
  font-size: smaller;
  padding: 10px;
}
.question-card__extra__badge {
  float: right;
}
</style>