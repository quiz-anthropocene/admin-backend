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

    <div v-if="quizzes && quizzes.length > 0">
      <router-link class="no-decoration" v-for="quiz in quizzes" :key="quiz.id" :to="{ name: 'quiz-detail', params: { quizId: quiz.id } }">
        <div class="category">
          <h3>{{ quiz.name }}</h3>
          <p><strong>{{ quiz.question_count }}</strong> question<span v-if="quiz.question_count > 1">s</span></p>
        </div>
      </router-link>
        <!-- <div class="col-sm">
          <router-link class="no-decoration" :to="{ name: 'quiz-detail', params: { quizId: quiz.id, skipIntro: true } }">
            <button class="btn btn-outline-primary">⏩&nbsp;Commencer le quiz !</button>
          </router-link>
        </div> -->
    </div>

    <br />
    <hr v-if="quizzes" />
    <div v-if="quizzes" class="row actions">
      <div class="col-sm">
        <router-link :to="{ name: 'question-list' }">
          ❓&nbsp;Toutes les questions
        </router-link>
        <br />
      </div>
      <div class="col-sm">
        <br />
      </div>
      <div class="col-sm">
        <HomeLink />
      </div>
    </div>
  </section>
</template>

<script>
import HomeLink from '../components/HomeLink.vue'

export default {
  name: 'QuizListPage',
  components: {
    HomeLink
  },

  data () {
    return {
      // quizzes: null,
    }
  },

  computed: {
    quizzes () {
      return this.$store.state.quizzes;
    },
  },

  mounted () {
  },

  methods: {
  }
}
</script>

<style scoped>
.category {
  width: 300px;
  display: inline-block;
  border: 1px solid var(--primary);
  border-radius: 5px;
  margin: 2.5px;
  padding: 5px;
  cursor: pointer;
}
</style>
