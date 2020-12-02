<template>
  <router-link class="card no-decoration" :to="{ name: 'quiz-detail', params: { quizId: quiz.id } }">
    <img class="card-img-top" v-bind:src="quiz.image_background_url || 'https://showyourstripes.info/stripes/GLOBE---1850-2019-MO.png'" alt="Une image pour illustrer le quiz">
    <div class="card-body">
      <h2 class="card-title">{{ quiz.name }}</h2>
      <p class="card-text text-center">
        <strong>{{ quiz.questions.length }}</strong> question<span v-if="quiz.questions.length > 1">s</span>
        <button class="btn btn-outline-primary btn-sm margin-0 margin-left-20">Découvrir</button>
      </p>
    </div>
    <div class="card-footer small d-none d-md-block">
      📝&nbsp;Auteur<span class="label label-hidden"><strong>{{ quiz.author }}</strong></span>
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
