<template>
  <section>
    <br />
    <div class="question" v-if="question">
      <h2>
        <span>Question #{{ question.id }}</span>
        <span> | </span>
        <span>Difficulté: <DifficultyBadge v-bind:difficulty="question.difficulty" /></span>
      </h2>
      <h3>{{ question.text }}</h3>
      <form v-on:submit="submitQuestion">
        <p :class="{ 'color-blue' : answerPicked === 'a' }">
          <input type="radio" id="one" value="a" v-model="answerPicked" :disabled="questionSubmitted">
          <label for="one">&nbsp;{{ question.answer_option_a }}</label>
        </p>
        <p :class="{ 'color-blue' : answerPicked === 'b' }">
          <input type="radio" id="two" value="b" v-model="answerPicked" :disabled="questionSubmitted">
          <label for="two">&nbsp;{{ question.answer_option_b }}</label>
        </p>
        <p :class="{ 'color-blue' : answerPicked === 'c' }">
          <input type="radio" id="three" value="c" v-model="answerPicked" :disabled="questionSubmitted">
          <label for="three">&nbsp;{{ question.answer_option_c }}</label>
        </p>
        <p :class="{ 'color-blue' : answerPicked === 'd' }">
          <input type="radio" id="four" value="d" v-model="answerPicked" :disabled="questionSubmitted">
          <label for="four">&nbsp;{{ question.answer_option_d }}</label>
        </p>
        <p>
          <button type="submit" class="button" :disabled="questionSubmitted || !answerPicked">Valider</button>
        </p>
      </form>
    </div>

    <br v-if="question && questionSubmitted" />

    <div class="answer" v-if="question && questionSubmitted">
      <h2 v-if="questionSuccess">C'est exact !</h2>
      <h2 v-if="!questionSuccess">Pas tout à fait...</h2>
      <h3 v-if="!questionSuccess">La réponse était: {{ question["answer_option_" + question["answer_correct"]] }}</h3>
      <p>ℹ️{{ question.answer_explanation }}</p>
      <p>🔗<a v-bind:href="question.answer_additional_links" target="_blank">{{ question.answer_additional_links }}</a></p>
    </div>

    <br />

    <div>
      <router-link :to="{ name: 'home' }">
        <button class="button">🏠Menu principal</button>
      </router-link>
      
      <router-link :to="{ name: 'question-detail', params: { questionId: questionRandomNextId } }">
        <button class="button">🔀Question au hasard</button>
      </router-link>
    </div>
  </section>
</template>

<script>
// import QuestionCard from './QuestionCard.vue'
import DifficultyBadge from './DifficultyBadge.vue'

export default {
  name: 'QuestionDetail',
  components: {
    // QuestionCard,
    DifficultyBadge,
  },

  data() {
    return {
      question: null,
      answerPicked: '',
      questionSubmitted: false,
      questionSuccess: false,
      questionRandomNextId: null,
      loading: false,
      error: null,
    }
  },

  created () {
    this.init(this.$route.params.questionId);
  },

  beforeRouteUpdate (to, from, next) {
    this.init(this.questionRandomNextId);
    next();
  },

  methods: {
    init(currentQuestionId) {
      this.answerPicked = '';
      this.questionSubmitted = false;
      this.questionSuccess = false;
      this.loading = false;
      this.error = null;
      this.fetchQuestion(currentQuestionId);
      this.fetchQuestionRandomNext(currentQuestionId);
    },
    fetchQuestion(questionId) {
      this.error = this.question = null;
      this.loading = true;
      fetch(`http://localhost:8000/api/questions/${questionId}`)
        .then(response => {
          this.loading = false
          return response.json()
        })
        .then(data => {
          this.question = data
        })
        .catch(err => {
          console.log(err)
        })
    },
    fetchQuestionRandomNext(currentQuestionId) {
      const params = { current: currentQuestionId };
      const urlParams = new URLSearchParams(Object.entries(params));
      fetch(`http://localhost:8000/api/questions/random?${urlParams}`)
        .then(response => {
          this.loading = false
          return response.json()
        })
        .then(data => {
          this.questionRandomNextId = data.id
        })
        .catch(err => {
          console.log(err)
        })
    },
    submitQuestion() {
      this.questionSubmitted = true;
      this.questionSuccess = (this.answerPicked === this.question.answer_correct);
    }
  }
}
</script>

<style scoped>
.question {
  border: 2px solid #005995;
  border-radius: 5px;
  padding-left: 10px;
  padding-right: 10px;
}

.answer {
  border: 2px solid #F33F3F;
  border-radius: 5px;
  padding-left: 10px;
  padding-right: 10px;
}
</style>