<template>
  <section>
    <br />

    <QuestionAnswerCards v-if="question" v-bind:question="question" v-bind:context="{ question_number: question.id }" @answerSubmitted="answerSubmitted($event)" />

    <div v-if="question" class="small" :key="question.id"> <!-- INFO: :key is to force reload, avoid button staying blur -->
      <br />
      <router-link v-if="questionSameCategoryNextId" :to="{ name: 'question-detail', params: { questionId: questionSameCategoryNextId } }">
        <button class="btn btn-outline-primary">⏩&nbsp;Autre question <span class="text-secondary">{{ question.category }}</span></button>
      </router-link>
      <router-link v-if="questionRandomNextId" :to="{ name: 'question-detail', params: { questionId: questionRandomNextId } }">
        <button class="btn btn-outline-primary">🔀&nbsp;Question au hasard</button>
      </router-link>
    </div>

    <br />
    <hr v-if="question" />
    <div v-if="question" class="row actions">
      <div class="col-sm">
        <router-link :to="{ name: 'contribute' }">
          ✍️&nbsp;Ajouter une question
        </router-link>
      </div>
      <div class="col-sm">
        <router-link :to="{ name: 'category-detail', params: { categoryName: question.category }  }">
          📂&nbsp;Toutes les questions <span class="text-secondary">{{ question.category }}</span>
        </router-link>
      </div>
      <div class="col-sm">
         <HomeLink />
      </div>
    </div>
  </section>
</template>

<script>
import QuestionAnswerCards from '../components/QuestionAnswerCards.vue'
import HomeLink from '../components/HomeLink.vue'

export default {
  name: 'Page',
  components: {
    QuestionAnswerCards,
    HomeLink,
  },

  data() {
    return {
      // question: null,
      questionSameCategoryNextId: null,
      questionRandomNextId: null,
    }
  },

  computed: {
    // currentQuestionId () {
    //   return this.$route.params.questionId;
    // },
    question () {
      return this.$store.getters.getQuestionById(this.$route.params.questionId);
    },
  },

  watch: {
    question: {
      immediate: true,
      // eslint-disable-next-line
      handler(newQuestion, oldQuestion) {
        if (newQuestion) {
          this.fetchQuestionRandomNext(this.question.id, this.question.category);
          this.fetchQuestionRandomNext(this.question.id);
        }
      }
    }
  },

  mounted () {
  },

  methods: {
    fetchQuestionRandomNext(currentQuestionId, currentQuestionCategory = null) {
      const params = { 'current': currentQuestionId };
      if (currentQuestionCategory) {
        params['category'] = currentQuestionCategory;
      }
      const urlParams = new URLSearchParams(Object.entries(params));
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/questions/random?${urlParams}`)
        .then(response => {
          return response.json()
        })
        .then(data => {
          if (currentQuestionCategory) {
            this.questionSameCategoryNextId = data.id;
          } else {
            this.questionRandomNextId = data.id;
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    answerSubmitted() {
    }
  }
}
</script>

<style scoped>
.question {
  border: 2px solid var(--primary);
  border-radius: 5px;
  padding: 10px;
}

.answer {
  border: 2px solid;
  border-radius: 5px;
  padding-left: 10px;
  padding-right: 10px;
  overflow: hidden;
}
.answer-success {
  border-color: green;
  background-color: #f2f8f2;
}
.answer-error {
  border-color: red;
  background-color: #fff2f2;
}
.answer p.answer-image {
  height: 300px;
}
.answer p.answer-image img {
  max-height: 100%;
  max-width: 100%;
  margin: auto;
}

@media all and (min-width: 60em) {
  .answer p.answer-image {
    height: 500px;
  }
}
</style>
