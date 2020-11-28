<template>
  <section>
    <router-link class="card no-decoration" :to="{ name: 'quiz-detail', params: { quizId: quiz.id } }">
      <img class="card-img-top" v-bind:src="quiz.image_background_url || 'https://showyourstripes.info/stripes/GLOBE---1850-2019-MO.png'" alt="Une image pour illustrer le quiz">
      <div class="card-body">
        <h2 class="card-title">{{ quiz.name }}</h2>
        <p class="card-subtitle"><strong>{{ quiz.questions.length }}</strong> question<span v-if="quiz.questions.length > 1">s</span></p>
        <button class="btn btn-outline-primary btn-lg btn-block">Découvrir le quiz</button>
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
  </section>
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
