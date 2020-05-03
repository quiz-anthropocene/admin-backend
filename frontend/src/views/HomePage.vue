<template>
  <section>
    <div class="alert alert-warning" role="alert">
      <i v-if="questionsCount">Il y a actuellement {{ questionsCount }} questions. </i>
      <i><router-link :to="{ name: 'about' }">Aidez-nous</router-link> à en rajouter plus !</i>
    </div>

    <div class="jumbotron jumbotron-fluid">
      <div class="container">
        <div class="row">
          <div class="col-sm padding-top-bottom-15">
            <svg class="bi bi-clipboard-data text-primary" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M4 1.5H3a2 2 0 00-2 2V14a2 2 0 002 2h10a2 2 0 002-2V3.5a2 2 0 00-2-2h-1v1h1a1 1 0 011 1V14a1 1 0 01-1 1H3a1 1 0 01-1-1V3.5a1 1 0 011-1h1v-1z" clip-rule="evenodd"/>
              <path fill-rule="evenodd" d="M9.5 1h-3a.5.5 0 00-.5.5v1a.5.5 0 00.5.5h3a.5.5 0 00.5-.5v-1a.5.5 0 00-.5-.5zm-3-1A1.5 1.5 0 005 1.5v1A1.5 1.5 0 006.5 4h3A1.5 1.5 0 0011 2.5v-1A1.5 1.5 0 009.5 0h-3z" clip-rule="evenodd"/>
              <path d="M4 11a1 1 0 112 0v1a1 1 0 11-2 0v-1zm6-4a1 1 0 112 0v5a1 1 0 11-2 0V7zM7 9a1 1 0 012 0v3a1 1 0 11-2 0V9z"/>
            </svg>
            <h3>
              Des questions objectives et sourcées<br />
              <small>(on fait de notre mieux :)</small>
            </h3>
          </div>
          <div class="col-sm padding-top-bottom-15">
            <svg class="bi bi-tag text-secondary" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M.5 2A1.5 1.5 0 012 .5h4.586a1.5 1.5 0 011.06.44l7 7a1.5 1.5 0 010 2.12l-4.585 4.586a1.5 1.5 0 01-2.122 0l-7-7A1.5 1.5 0 01.5 6.586V2zM2 1.5a.5.5 0 00-.5.5v4.586a.5.5 0 00.146.353l7 7a.5.5 0 00.708 0l4.585-4.585a.5.5 0 000-.708l-7-7a.5.5 0 00-.353-.146H2z" clip-rule="evenodd"/>
              <path fill-rule="evenodd" d="M2.5 4.5a2 2 0 114 0 2 2 0 01-4 0zm2-1a1 1 0 100 2 1 1 0 000-2z" clip-rule="evenodd"/>
            </svg>
            <h3>
              Explorer et filtrer grâce aux <span class="text-secondary">catégories</span> & <span class="color-tag">tags</span>
              <!-- <small>(tags à venir)</small> -->
            </h3>
          </div>
          <div class="col-sm padding-top-bottom-15">
            <svg class="bi bi-arrow-repeat text-success" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M2.854 7.146a.5.5 0 00-.708 0l-2 2a.5.5 0 10.708.708L2.5 8.207l1.646 1.647a.5.5 0 00.708-.708l-2-2zm13-1a.5.5 0 00-.708 0L13.5 7.793l-1.646-1.647a.5.5 0 00-.708.708l2 2a.5.5 0 00.708 0l2-2a.5.5 0 000-.708z" clip-rule="evenodd"/>
              <path fill-rule="evenodd" d="M8 3a4.995 4.995 0 00-4.192 2.273.5.5 0 01-.837-.546A6 6 0 0114 8a.5.5 0 01-1.001 0 5 5 0 00-5-5zM2.5 7.5A.5.5 0 013 8a5 5 0 009.192 2.727.5.5 0 11.837.546A6 6 0 012 8a.5.5 0 01.501-.5z" clip-rule="evenodd"/>
            </svg>
            <h3>
              À l'écoute de vos retours<br />
              <small>et ouverts aux contributions !</small>
            </h3>
          </div>
        </div>
      </div>
    </div>

    <br />

    <div class="row justify-content-md-center">
      <div class="col-sm-4" v-if="questionsCount">
        <router-link class="no-decoration" :to="{ name: 'quiz-list' }">
          <button class="btn btn-outline-primary btn-lg btn-block">
            🕹&nbsp;<strong>Tous les quiz</strong>
          </button>
        </router-link>
      </div>
      <div class="col-sm-4" v-if="questionSameFilterNextId">
        <router-link class="no-decoration" :to="{ name: 'question-detail', params: { questionId: questionSameFilterNextId } }">
          <button class="btn btn-outline-primary btn-lg btn-block">🔀&nbsp;<strong>Une question au hasard</strong></button>
        </router-link>
      </div>
      <div class="col-sm-4" v-if="questionsCount">
        <router-link class="no-decoration" :to="{ name: 'question-list' }">
          <button class="btn btn-outline-primary btn-lg btn-block">❓&nbsp;<strong>Toutes les questions</strong></button>
        </router-link>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'HomePage',

  data () {
    return {
      questionSameFilterNextId: null,
    }
  },

  computed: {
    questionsCount () {
      return this.$store.state.questions.length;
    }
  },

  watch: {
    questionsCount: {
      immediate: true,
      // eslint-disable-next-line
      handler(newQuestionsCount, oldQuestionsCount) {
        if (newQuestionsCount) {
          this.questionSameFilterNextId = this.$store.getters.getNextQuestionByFilter().id;
        }
      }
    }
  },

  mounted () {
  },

  methods: {
  }
}
</script>

<style scoped>
svg {
  font-size: 2em;
}

.jumbotron {
  padding-top: 1em;
  padding-bottom: 1em;
  margin-bottom: 1em;
}
.jumbotron .row .col:hover {
  transform: scale(1.03);
}

.row > .col-sm-4 {
  padding-bottom: 20px;
}

.btn-lg {
  line-height: 3;
}
</style>
