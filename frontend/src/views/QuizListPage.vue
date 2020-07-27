<template>
  <section>
    <!-- Header -->
    <section class="filter-box">
      <div class="filter-box--header">
        <div class="text-align-right">
          <span class="label label-hidden"><strong>{{ quizzes.length }}</strong> Quiz</span>
        </div>
      </div>
    </section>

    <div v-if="quizzes && quizzes.length === 0">
      Pas de quiz :(
    </div>

    <div v-if="quizzes && quizzes.length > 0" class="row">
      <div class="col-sm-6" v-for="quiz in quizzes" :key="quiz.id">
        <router-link class="card no-decoration" :to="{ name: 'quiz-detail', params: { quizId: quiz.id } }">
          <img v-bind:src="quiz.image_background_url || 'https://showyourstripes.info/stripes/GLOBE---1850-2019-MO.png'" class="card-img-top" alt="Une image pour illustrer le quiz">
          <div class="card-body">
            <h2>{{ quiz.name }}</h2>
            <p><strong>{{ quiz.questions.length }}</strong> question<span v-if="quiz.questions.length > 1">s</span></p>
            <hr />
            <div class="row small">
              <div v-if="quiz.categories_list && quiz.categories_list.length > 0" title="Catégorie(s) du quiz">
                📂
                <span v-for="(category, index) in quiz.categories_list" :key="category">
                  <span v-if="index < 3" class="label label-category">{{ category }}</span>
                </span>
              </div>
              <div class="label label-hidden">📝&nbsp;Auteur:&nbsp;<strong>{{ quiz.author }}</strong></div>
            </div>
          </div>
        </router-link>
      </div>
        <!-- <div class="col-sm">
          <router-link class="no-decoration" :to="{ name: 'quiz-detail', params: { quizId: quiz.id, skipIntro: true } }">
            <button class="btn btn-outline-primary">⏩&nbsp;Commencer le quiz !</button>
          </router-link>
        </div> -->
    </div>
  </section>
</template>

<script>
export default {
  name: 'QuizListPage',
  metaInfo: {
    title: 'Tous les quiz',
    meta: [
      { property: 'og:title', vmid: 'og:title', content: 'Tous les quiz' },
      { property: 'twitter:title', vmid: 'twitter:title', content: 'Tous les quiz' },
    ],
  },
  components: {
  },

  data() {
    return {
      // quizzes: null,
    };
  },

  computed: {
    quizzes() {
      return this.$store.state.quizzes;
    },
  },

  mounted() {
  },

  methods: {
  },
};
</script>

<style scoped>
.filter-box {
  box-shadow: 0px 0px 5px 5px #dfdfdf;
  border-radius: 5px;
  margin: 10px 0px;
  padding: 10px;
  max-height: 80vh;
  overflow: auto;
}
.filter-box > .filter-box--header {
  text-align: left;
  cursor: pointer;
}

.row > .col-sm-6 {
  padding-bottom: 20px;
}

.card:hover {
  box-shadow: 0px 0px 5px 5px #dfdfdf;
  transition: 0.2s;
}
</style>
