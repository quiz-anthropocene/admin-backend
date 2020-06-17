<template>
  <section>
    <br />

    <h2>
      Tous les quiz&nbsp;
      <span v-if="quizzes" class="text-secondary"><small>{{ quizzes.length }}</small></span>
    </h2>

    <br />

    <div v-if="quizzes && quizzes.length === 0">
      Pas de quiz :(
    </div>

    <div v-if="quizzes && quizzes.length > 0" class="row">
      <div class="col-sm-6" v-for="quiz in quizzes" :key="quiz.id">
        <router-link class="card no-decoration" :to="{ name: 'quiz-detail', params: { quizId: quiz.id } }">
          <img v-bind:src="quiz.image_background_url || 'https://www.climatecentral.org/uploads/general/show-your-stripes-header-1000x169.jpg'" class="card-img-top" alt="Une image pour illustrer le quiz">
          <div class="card-body">
            <h2>{{ quiz.name }}</h2>
            <p><strong>{{ quiz.question_count }}</strong> question<span v-if="quiz.question_count > 1">s</span></p>
            <hr />
            <div class="row small">
              <div v-if="quiz.categories_list && quiz.categories_list.length > 0" title="Catégorie(s) du quiz">
                📂
                <span v-for="(category, index) in quiz.categories_list" :key="category">
                  <span v-if="index < 3" class="label label-category">{{ category }}</span>
                </span>
              </div>
              <div class="label label-hidden">📝&nbsp;Auteur:&nbsp;{{ quiz.author }}</div>
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
.row > .col-sm-6 {
  padding-bottom: 20px;
}

.card:hover {
  box-shadow: 0px 0px 5px 5px #dfdfdf;
  transition: 0.2s;
}
</style>
