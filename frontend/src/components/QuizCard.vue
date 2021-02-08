<template>
  <router-link class="card no-decoration" :to="{ name: 'quiz-detail', params: { quizId: quiz.id } }">
    <img class="card-img-top" v-bind:src="quiz.image_background_url || 'https://quizanthropocene.fr/showyourstripes_globe_1850-2019.png'" alt="Une image pour illustrer le quiz">
    <div class="card-body">
      <h2 class="card-title">
        {{ quiz.name }}
        <span v-if="quiz.has_audio" class="label small" style="vertical-align:top">🔉Audio</span>
      </h2>
      <p class="card-text text-center">
        <strong>{{ quiz.questions.length }}</strong> question<span v-if="quiz.questions.length > 1">s</span>
        <button class="btn btn-outline-primary btn-sm margin-0 margin-left-20">Découvrir</button>
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
    // eslint-disable-next-line
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
.card-body button {
  margin-top: 16px;
}
</style>
