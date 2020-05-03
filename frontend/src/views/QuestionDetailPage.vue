<template>
  <section>
    <QuestionAnswerCards v-if="question && questionsDisplayedCount" v-bind:question="question" v-bind:context="{ question_number: (questionIndex+1)+' / '+questionsDisplayedCount, source: 'question' }" @answerSubmitted="answerSubmitted($event)" />

    <div v-if="question" class="small" :key="question.id"> <!-- INFO: :key is to force reload, avoid button staying blur -->
      <!-- <br /> -->
      <router-link v-if="questionSameFilterNextId" :to="{ name: 'question-detail', params: { questionId: questionSameFilterNextId } }">
        <button class="btn" :class="emphasisNextButton ? 'btn-primary' : 'btn-outline-primary'">⏩&nbsp;Question suivante</button>
      </router-link>
    </div>
  </section>
</template>

<script>
import QuestionAnswerCards from '../components/QuestionAnswerCards.vue'

export default {
  name: 'Page',
  components: {
    QuestionAnswerCards,
  },

  data() {
    return {
      emphasisNextButton: false,
      questionSameFilterNextId: null,
    }
  },

  computed: {
    question () {
      return this.$store.getters.getQuestionById(parseInt(this.$route.params.questionId));
    },
    questionIndex () {
      return this.$store.getters.getCurrentQuestionIndex(parseInt(this.$route.params.questionId));
    },
    questionFilters () {
      return this.$store.state.questionFilters;
    },
    questionsDisplayedCount () {
      return this.$store.state.questionsDisplayed.length;
    },
  },

  watch: {
    question: {
      immediate: true,
      // eslint-disable-next-line
      handler(newQuestion, oldQuestion) {
        if (newQuestion) {
          this.emphasisNextButton = false;
          this.questionSameFilterNextId = this.$store.getters.getNextQuestionByFilter(newQuestion.id).id;
        }
      }
    },
    // eslint-disable-next-line
    questionFilters (newQuestionFilters, oldQuestionFilters) {
      if (newQuestionFilters) {
        const _nextQuestion = this.$store.getters.getNextQuestionByFilter();
        this.$router.push({ name: 'question-detail', params: { questionId: _nextQuestion.id } });
      }
    }
  },

  mounted () {
  },

  methods: {
    // eslint-disable-next-line
    answerSubmitted(data) {
      this.emphasisNextButton = true; // !this.emphasisNextButton;
    }
  }
}
</script>

<style scoped>
</style>
