<template>
  <section>
    <!-- Header -->
    <QuestionFilter objectType="quiz" :counter="quizzesDisplayed.length" />

    <div v-if="quizzesDisplayed && quizzesDisplayed.length === 0">
      {{ $t('messages.noQuiz') }}
    </div>

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
      return this.$store.state.quizzesDisplayed
        .slice(0) // .slice makes a copy of the array, instead of mutating the orginal
        .sort((a, b) => a.name.localeCompare(b.name));
    },
  },

  watch: {
    // eslint-disable-next-line
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
