<template>
  <section>
    <h2 class="text-align-left">{{ $t('messages.allQuizs') }}</h2>

    <QuestionFilter objectType="quiz" :counter="quizsDisplayed.length" />

    <section v-if="quizsDisplayed && quizsDisplayed.length === 0" class="alert alert-warning" role="alert">
      🙁{{ $t('messages.noQuizFound') }}
    </section>

    <div v-if="quizsDisplayed && quizsDisplayed.length > 0" id="quiz-list" class="row">
      <div class="col-sm-4" v-for="quiz in quizsDisplayed" :key="quiz.id">
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
      // quizsDisplayed: null,
    };
  },

  computed: {
    quizsDisplayed() {
      return this.$store.state.quizsDisplayed;
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
.row > .col-sm-4 {
  padding-bottom: 15px;
}
.row > .col-sm-4 > .card {
  height: 100%;
}
</style>
