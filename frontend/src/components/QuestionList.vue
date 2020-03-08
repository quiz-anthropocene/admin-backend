<template>
  <section>
    <div class="help">
      <i v-if="questions">Il y a actuellement {{ questions.length }} questions. </i>
      <i><router-link :to="{ name: 'about' }">Aidez-nous</router-link> à en rajouter plus !</i>
    </div>
    <br />

    <!-- Filtre: catégorie -->
    <div>
      <span class="category" v-for="category in categories" :key="category" :class="{ 'category-active' : category === categorySelected }" @click="clickCategory(category)">{{ category }}</span>
    </div>

    <br />

    <div v-if="loading" class="loading">
      Loading...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <!-- Question List -->
    <div v-if="questions" class="row">
      <div class="row-item" v-for="question in questionsDisplayed" :key="question">
        <router-link class="no-decoration" :to="{ name: 'question-detail', params: { questionId: question.id } }">
          <QuestionCard v-bind:question="question" />
        </router-link>
      </div>
    </div>
  </section>
</template>

<script>
import QuestionCard from './QuestionCard.vue'

export default {
  name: 'QuestionList',
  components: {
    QuestionCard,
  },

  data () {
    return {
      categories: ['action', 'biodiversité', 'climat', 'consommation', 'énergie', 'histoire', 'pollution', 'ressources', 'science', 'autre'],
      categorySelected: null,
      questions: null,
      questionsDisplayed: null,
      loading: false,
      error: null,
    }
  },

  created () {
    this.fetchQuestions()
  },

  methods: {
    fetchQuestions() {
      this.error = this.questions = this.questionsDisplayed = null
      this.loading = true
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/questions`)
        .then(response => {
          this.loading = false
          return response.json()
        })
        .then(data => {
          this.questions = this.questionsDisplayed = data
        })
        .catch(err => {
          console.log(err)
        })
    },
    clickCategory(category) {
      this.categorySelected = (this.categorySelected === category) ? null : category;
      this.updateQuestionsDisplayed(this.categorySelected);
    },
    updateQuestionsDisplayed(categorySelection) {
      if (categorySelection) {
        this.questionsDisplayed = this.questions.filter(q => q.category === categorySelection);
      } else {
        this.questionsDisplayed = this.questions;
      }
    }
  }
}
</script>

<style scoped>
.category {
  display: inline-block;
  border: 1px solid #F33F3F;
  border-radius: 5px;
  margin: 5px;
  padding: 5px;
  cursor: pointer;
}
.category:hover {
  background-color: #f88787;
}
.category-active {
  background-color: #f88787;
  text-shadow: 0px 0px 1px black;
}

.row {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}
.row-item {
  flex: 0 1 100%;
  height: 150px;
  margin-bottom: 10px;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: 0.1s;
  border: 2px solid #005995;
  border-radius: 5px;
  cursor: pointer;
}
.row-item:hover {
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}

@media all and (min-width: 40em) {
  .row-item {
    max-width: calc(50% - 1em);
  }
}
@media all and (min-width: 60em) {
  .row-item {
    max-width: calc(33.33% - 1em);
  }
}
</style>
