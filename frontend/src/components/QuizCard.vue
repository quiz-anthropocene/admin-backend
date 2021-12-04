<template>
  <router-link class="card no-decoration" :to="{ name: 'quiz-detail', params: { quizId: quiz.slug || quiz.id } }">
    <img class="card-img-top" v-bind:src="quiz.image_background_url || 'https://quizanthropocene.fr/showyourstripes_globe_1850-2019.png'" alt="Une image pour illustrer le quiz">
    <div class="card-body">
      <h3 class="card-title">
        {{ quiz.name }}
        <span v-if="quiz.has_audio" class="label small" style="vertical-align:top">🔉Audio</span>
      </h3>
      <p class="card-text text-center d-none d-sm-block">
        <strong>{{ quiz.questions.length }}</strong> question<span v-if="quiz.questions.length > 1">s</span>
        <!-- <button class="btn btn-outline-primary btn-sm margin-0 margin-left-20">{{ $t('messages.discover') }}</button> -->
      </p>
    </div>
  </router-link>
</template>

<script>
export default {
  name: 'QuizCard',
  components: {
  },
  props: {
    quiz: { type: Object },
  },
  data() {
    return {
    };
  },

  computed: {
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
.card:hover {
  box-shadow: 0px 0px 5px 5px #dfdfdf;
  transition: 0.2s;
}
.card-img-top {
  /* default: 7.5vw */
  height: 10vw;
}
.card-body button {
  margin-top: 16px;
}
</style>
