<template>
  <section>
    <!-- Header -->
    <QuestionFilter objectType="quiz" :counter="quizzesDisplayed.length" />

    <section v-if="quizzesDisplayed && quizzesDisplayed.length === 0" class="alert alert-warning" role="alert">
      🙁{{ $t('messages.noQuizFound') }}
    </section>

    <div v-if="quizzesDisplayed && quizzesDisplayed.length > 0" id="quiz-list" class="row">
      <div class="col-sm-6" v-for="quiz in quizzesDisplayed" :key="quiz.id">
        <QuizCard :quiz="quiz" />
      </div>
        <!-- <div class="col-sm">
          <router-link class="no-decoration" :to="{ name: 'quiz-detail', params: { quizId: quiz.id, skipIntro: true } }">
            <button class="btn btn-outline-primary">⏩&nbsp;{{ $t('messages.startQuiz') }}</button>
          </router-link>
        </div> -->
    </div>
  </section>
</template>

<script>
import { metaTagsGenerator } from '../utils';
import QuestionFilter from '../components/QuestionFilter.vue';
import QuizCard from '../components/QuizCard.vue';

export default {
  name: 'QuizListPage',
  metaInfo() {
    const title = 'Tous les quiz';
    return {
      meta: metaTagsGenerator(title),
    };
  },
  components: {
    QuestionFilter,
    QuizCard,
  },

  data() {
    return {
      // quizzesDisplayed: null,
    };
  },

  computed: {
    quizzesDisplayed() {
      return this.$store.state.quizzesDisplayed;
    },
  },

  watch: {
  },

  mounted() {
  },

  methods: {
  },
};
</script>

<style scoped>
.row > .col-sm-6 {
  padding-bottom: 15px;
}
.row > .col-sm-6 > .card {
  height: 100%;
}
</style>
