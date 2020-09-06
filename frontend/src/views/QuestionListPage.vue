<template>
  <section>
    <!-- Question List -->
    <div v-if="questionsDisplayed" id="question-list" class="row">
      <div class="col-lg-4 col-sm-6" v-for="question in questionsDisplayed" :key="question.id">
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
import { metaTagsGenerator } from '../utils';
import QuestionPreviewCard from '../components/QuestionPreviewCard.vue';

export default {
  name: 'QuestionListPage',
  metaInfo() {
    const title = 'Toutes les questions';
    return {
      meta: metaTagsGenerator(title),
    };
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
.row > .col-lg-4,
.row > .col-sm-6 {
  padding-bottom: 15px;
}
</style>
