<template>
  <section>
    <div class="alert alert-warning">
      <i v-if="questionStats">Il y a actuellement {{ questionStats["publish"][0]["count"] }} questions. </i>
      <i><router-link :to="{ name: 'about' }">Aidez-nous</router-link> à en rajouter plus !</i>
    </div>

    <div class="jumbotron jumbotron-fluid">
      <div class="container">
        <!-- <h1 class="display-4">Fluid jumbotron</h1>
        <p class="lead">This is a modified jumbotron that occupies the entire horizontal space of its parent.</p> -->
        <div class="row">
          <div class="col-sm padding-top-bottom-15">
            <svg class="bi bi-clipboard-data text-primary" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M4 1.5H3a2 2 0 00-2 2V14a2 2 0 002 2h10a2 2 0 002-2V3.5a2 2 0 00-2-2h-1v1h1a1 1 0 011 1V14a1 1 0 01-1 1H3a1 1 0 01-1-1V3.5a1 1 0 011-1h1v-1z" clip-rule="evenodd"/>
              <path fill-rule="evenodd" d="M9.5 1h-3a.5.5 0 00-.5.5v1a.5.5 0 00.5.5h3a.5.5 0 00.5-.5v-1a.5.5 0 00-.5-.5zm-3-1A1.5 1.5 0 005 1.5v1A1.5 1.5 0 006.5 4h3A1.5 1.5 0 0011 2.5v-1A1.5 1.5 0 009.5 0h-3z" clip-rule="evenodd"/>
              <path d="M4 11a1 1 0 112 0v1a1 1 0 11-2 0v-1zm6-4a1 1 0 112 0v5a1 1 0 11-2 0V7zM7 9a1 1 0 012 0v3a1 1 0 11-2 0V9z"/>
            </svg>
            <h3>Des questions objectives et sourcées</h3>
          </div>
          <div class="col-sm padding-top-bottom-15">
            <svg class="bi bi-tag text-secondary" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M.5 2A1.5 1.5 0 012 .5h4.586a1.5 1.5 0 011.06.44l7 7a1.5 1.5 0 010 2.12l-4.585 4.586a1.5 1.5 0 01-2.122 0l-7-7A1.5 1.5 0 01.5 6.586V2zM2 1.5a.5.5 0 00-.5.5v4.586a.5.5 0 00.146.353l7 7a.5.5 0 00.708 0l4.585-4.585a.5.5 0 000-.708l-7-7a.5.5 0 00-.353-.146H2z" clip-rule="evenodd"/>
              <path fill-rule="evenodd" d="M2.5 4.5a2 2 0 114 0 2 2 0 01-4 0zm2-1a1 1 0 100 2 1 1 0 000-2z" clip-rule="evenodd"/>
            </svg>
            <h3>Explorer et filtrer grâce aux catégories <small>(tags à venir)</small></h3>
          </div>
          <div class="col-sm padding-top-bottom-15">
            <svg class="bi bi-arrow-repeat text-warning" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M2.854 7.146a.5.5 0 00-.708 0l-2 2a.5.5 0 10.708.708L2.5 8.207l1.646 1.647a.5.5 0 00.708-.708l-2-2zm13-1a.5.5 0 00-.708 0L13.5 7.793l-1.646-1.647a.5.5 0 00-.708.708l2 2a.5.5 0 00.708 0l2-2a.5.5 0 000-.708z" clip-rule="evenodd"/>
              <path fill-rule="evenodd" d="M8 3a4.995 4.995 0 00-4.192 2.273.5.5 0 01-.837-.546A6 6 0 0114 8a.5.5 0 01-1.001 0 5 5 0 00-5-5zM2.5 7.5A.5.5 0 013 8a5 5 0 009.192 2.727.5.5 0 11.837.546A6 6 0 012 8a.5.5 0 01.501-.5z" clip-rule="evenodd"/>
            </svg>
            <h3>À l'écoute de vos retours et ouverts aux contributions !</h3>
          </div>
        </div>
      </div>
    </div>

    <div class="row justify-content-md-center">
      <div class="col col-6">
        <router-link :to="{ name: 'question-detail', params: { questionId: questionRandomNextId } }" class="no-decoration">
          <button class="btn btn-outline-primary btn-lg btn-block">🔀&nbsp;<strong>Question au hasard</strong></button>
        </router-link>
      </div>
    </div>

    <br />

    <div class="row">
      <div class="col-sm">
        <router-link :to="{ name: 'question-list' }">
          Toutes les questions
        </router-link>
      </div>
      <div class="col-sm">
        <router-link :to="{ name: 'category-list' }">
          Toutes les catégories
        </router-link>
      </div>
      <div class="col-sm">
        Tous les quizz <small>(à venir)</small>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'HomePage',

  data () {
    return {
      questionStats: null,
      questionRandomNextId: null,
      loading: false,
      error: null,
    }
  },

  mounted () {
    this.fetchQuestionStats();
    this.fetchQuestionRandomNext();
  },

  methods: {
    fetchQuestionStats() {
      this.error = this.questionStats = null
      this.loading = true
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/questions/stats`)
        .then(response => {
          this.loading = false
          return response.json()
        })
        .then(data => {
          this.questionStats = data
        })
        .catch(error => {
          console.log(error)
          this.error = error;
        })
    },
    fetchQuestionRandomNext() {
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/questions/random?`)
        .then(response => {
          this.loading = false
          return response.json()
        })
        .then(data => {
          this.questionRandomNextId = data.id;
        })
        .catch(error => {
          console.log(error)
          this.error = error;
        })
    },
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

.category {
  display: inline-block;
  border: 1px solid #F33F3F;
  border-radius: 5px;
  margin: 2.5px;
  padding: 5px;
  cursor: pointer;
}
.category-active {
  background-color: #f88787;
  text-shadow: 0px 0px 1px black;
}

.row-item-question {
  height: 150px;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: 0.1s;
  border: 2px solid #005995;
  border-radius: 5px;
  cursor: pointer;
}

@media(hover: hover) and (pointer: fine) {
  .category:hover {
    background-color: #f88787;
  }
  .row-item-question:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
  }
}
</style>
