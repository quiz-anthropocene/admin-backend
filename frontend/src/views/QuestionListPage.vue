<template>
  <section>
    <br />

    <!-- Question List -->
    <div v-if="questions" class="row">
      <div class="row-item row-item-question" v-for="question in questionsDisplayed" :key="question.id">
        <router-link class="no-decoration" :to="{ name: 'question-detail', params: { questionId: question.id } }">
          <QuestionPreviewCard v-bind:question="question" />
        </router-link>
      </div>
    </div>

    <br />
    <hr v-if="questions" />
    <div v-if="questions" class="row actions">
      <div class="col-sm">
        <router-link :to="{ name: 'category-list' }">
          📂&nbsp;Toutes les catégories
        </router-link>
        <br />
      </div>
      <div class="col-sm">
        <router-link :to="{ name: 'tag-list' }">
          🏷️&nbsp;Tous les tags
        </router-link>
        <br />
      </div>
      <div class="col-sm">
        <HomeLink />
      </div>
    </div>
  </section>
</template>

<script>
import QuestionPreviewCard from '../components/QuestionPreviewCard.vue'
import HomeLink from '../components/HomeLink.vue'

export default {
  name: 'QuestionListPage',
  components: {
    QuestionPreviewCard,
    HomeLink
  },

  data () {
    return {
      // questions: null,
      questionsDisplayed: null,
    }
  },

  computed: {
    questions () {
      return this.$store.state.questionsDisplayed;
    },
  },

  watch: {
    // eslint-disable-next-line
    questions (newQuestions, oldQuestions) {
      this.questionsDisplayed = newQuestions;
    }
  },

  mounted () {
    this.questionsDisplayed = this.questions;
  },

  methods: {
    // updateQuestionsDisplayed() {
    //   this.questionsDisplayed = this.$store.getters.getQuestionsByFilter({
    //     "categoryName": this.categorySelected,
    //     "tagName": this.tagSelected,
    //     "authorName": this.authorSelected,
    //     "difficulty": this.difficultySelected
    //   });
    // }
  }
}
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
