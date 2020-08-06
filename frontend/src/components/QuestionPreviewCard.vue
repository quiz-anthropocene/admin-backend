<template>
  <div class="question-card" :class="customClass">
    <!-- <div class="question-card__header"></div> -->
    <div class="question-card__content">
      <p>{{ question.text }}</p>
    </div>
    <hr class="custom-separator">
    <div class="question-card__extra">
      <span class="text-secondary">{{ question.category.name }}</span>
      <DifficultyBadge class="question-card__extra__badge" v-bind:difficulty="question.difficulty" />
    </div>
  </div>
</template>

<script>
import DifficultyBadge from './DifficultyBadge.vue';

export default {
  name: 'QuestionPreviewCard',
  props: {
    question: Object,
    customClass: String,
  },
  components: {
    DifficultyBadge,
  },
};
</script>

<style scoped>
.question-card {
  /* height: 100%; */
  height: 150px;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: 0.1s;
  border: 2px solid var(--primary);
  border-radius: 5px;
  overflow: hidden;
  cursor: pointer;
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
  text-align: left;
  font-size: smaller;
  padding: 10px;
}
.question-card__extra__badge {
  float: right;
}

.answer-success {
  border-color: green;
  background-color: #f2f8f2;
}
.answer-error {
  border-color: red;
  background-color: #fff2f2;
}

@media(hover: hover) and (pointer: fine) {
  .question-card:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
  }
}
</style>
