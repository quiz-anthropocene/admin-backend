<template>
  <section>
    <div class="help"><i>Il y a actuellement {{ questions.length }} questions. <a href="#">Aidez-nous</a> à en rajouter plus !</i></div>
    <br />

    <!-- Filtre: catégorie -->
    <div>
      <span class="category" v-for="category in categories" :key="category" :class="{ 'category-active' : category == category_selected }" @click="clickCategory(category)">{{ category }}</span>
    </div>

    <br />

    <div v-if="loading" class="loading">
      Loading...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="questions" class="row">
      <div class="row-item" v-for="question in questions_displayed" :key="question">
        <div class="question">{{ question.text }}</div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'QuestionsAll',
  props: {
    msg: String
  },

  data () {
    return {
      categories: ['action', 'biodiversité', 'climat', 'consommation', 'énergie', 'histoire', 'pollution', 'ressources', 'science', 'autre'],
      category_selected: null,
      questions: null,
      questions_displayed: null,
      loading: false,
      error: null,
    }
  },

  created () {
    this.fetchData()
  },

  methods: {
    fetchData () {
      this.error = this.questions = this.questions_displayed = null
      this.loading = true
      fetch("http://localhost:8000/api/questions")
        .then(response => {
          this.loading = false
          return response.json()
        })
        .then(data => {
          this.questions = this.questions_displayed = data
        })
        .catch(err => {
          console.log(err)
        })
    },
    clickCategory(category) {
      this.category_selected = (this.category_selected === category) ? null : category;
      this.updateQuestionsDisplayed(this.category_selected);
    },
    updateQuestionsDisplayed(category_selection) {
      if (category_selection) {
        this.questions_displayed = this.questions.filter(q => q.category === category_selection);
      } else {
        this.questions_displayed = this.questions;
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
  display: -webkit-flex;
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}
.row-item {
  flex: 0 1 100%;
  height: 150px;
  margin-bottom: 10px;
  overflow-y: hidden;
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

.question {
  padding: 10px;
}
</style>
