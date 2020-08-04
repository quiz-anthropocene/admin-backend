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
          <img class="card-img-top" v-bind:src="quiz.image_background_url || 'https://showyourstripes.info/stripes/GLOBE---1850-2019-MO.png'" alt="Une image pour illustrer le quiz">
          <div class="card-body">
            <h2 class="card-title">{{ quiz.name }}</h2>
            <p class="card-subtitle"><strong>{{ quiz.questions.length }}</strong> question<span v-if="quiz.questions.length > 1">s</span></p>
            <section class="d-none d-md-block">
              <hr class="margin-top-bottom-10" />
              <div class="small">
                <div class="label label-hidden">📝&nbsp;Auteur:&nbsp;<strong>{{ quiz.author }}</strong></div>
                <!-- <div v-if="quiz.categories_list && quiz.categories_list.length > 0" title="Catégorie(s) du quiz">
                  📂
                  <span v-for="(category, index) in quiz.categories_list" :key="category">
                    <span v-if="index < 3" class="label label-category">{{ category }}</span>
                  </span>
                </div> -->
                <!-- <div v-if="quiz.tags && quiz.tags.length > 0" title="Tag(s) du quiz">
                  🏷️&nbsp;<span v-for="(tag, index) in quiz.tags" :key="tag">
                    <span v-if="index < 3" class="label label-tag">{{ tag.name }}</span>
                  </span>
                </div> -->
              </div>
            </section>
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
      return this.$store.state.quizzes
        .slice(0) // .slice makes a copy of the array, instead of mutating the orginal
        .sort((a, b) => a.name.localeCompare(b.name));
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
  box-shadow: 0px 0px 5px 5px #c5c5c5;
  border-radius: 5px;
  margin: 10px 0px;
  padding: 5px;
}
.filter-box > .filter-box--header {
  text-align: left;
  cursor: pointer;
}

.row > .col-sm-6 {
  padding-bottom: 15px;
}

.card:hover {
  box-shadow: 0px 0px 5px 5px #dfdfdf;
  transition: 0.2s;
}
</style>
