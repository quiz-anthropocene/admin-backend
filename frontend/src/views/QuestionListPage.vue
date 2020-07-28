<template>
  <section>
    <!-- Question List -->
    <div v-if="questionsDisplayed" class="row">
      <div class="row-item row-item-question" v-for="question in questionsDisplayed" :key="question.id">
        <router-link class="no-decoration" :to="{ name: 'question-detail', params: { questionId: question.id } }">
          <QuestionPreviewCard v-bind:question="question" />
        </router-link>
      </div>
      <p v-if="questionsDisplayed.length === 0">
        Aucune question trouvée avec les filtres selectionnés.
      </p>
    </div>
  </section>
</template>

<script>
import QuestionPreviewCard from '../components/QuestionPreviewCard.vue';

export default {
  name: 'QuestionListPage',
  metaInfo: {
    title: 'Toutes les questions',
    meta: [
      { property: 'og:title', vmid: 'og:title', content: 'Toutes les questions' },
      { property: 'twitter:title', vmid: 'twitter:title', content: 'Toutes les questions' },
    ],
  },
  components: {
    QuestionPreviewCard,
  },

  data() {
    return {
    };
  },

  computed: {
    questionsDisplayed() {
      return this.$store.state.questionsDisplayed;
    },
  },
};
</script>

<style scoped>
.row-item-question {
  height: 150px;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: 0.1s;
  border: 2px solid var(--primary);
  border-radius: 5px;
  cursor: pointer;
}

@media(hover: hover) and (pointer: fine) {
  .row-item-question:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
  }
}
</style>
