<template>
  <section>
    <br />
    <div class="question" v-if="question">
      <p>
        <span>Question #{{ question.id }}</span>
        <span> | </span>
        <span>Difficulté: {{ question.difficulty }}</span>
      </p>
      <h3>{{ question.text }}</h3>
      <form v-on:submit="submitQuestion">
        <p>
          <input type="radio" id="one" value="a" v-model="answerPicked" :disabled="questionSubmitted">
          <label for="one">&nbsp;{{ question.answer_option_a }}</label>
        </p>
        <p>
          <input type="radio" id="two" value="b" v-model="answerPicked" :disabled="questionSubmitted">
          <label for="two">&nbsp;{{ question.answer_option_b }}</label>
        </p>
        <p>
          <input type="radio" id="three" value="c" v-model="answerPicked" :disabled="questionSubmitted">
          <label for="three">&nbsp;{{ question.answer_option_c }}</label>
        </p>
        <p>
          <input type="radio" id="four" value="d" v-model="answerPicked" :disabled="questionSubmitted">
          <label for="four">&nbsp;{{ question.answer_option_d }}</label>
        </p>
        <p>
          <input type="submit" value="Valider" :disabled="questionSubmitted || !answerPicked" />
        </p>
      </form>
    </div>
    <div v-if="question && questionSubmitted">
      <h2 v-if="questionSuccess">C'est exact !</h2>
      <h2 v-if="!questionSuccess">
        Pas tout à fait...<br>
        <small>La réponse était: {{ question["answer_option_" + question["answer_correct"]] }}</small>
      </h2>
      <p>ℹ️{{ question.answer_explanation }}</p>
      <p>🔗<a v-bind:href="question.answer_additional_links" target="_blank">{{ question.answer_additional_links }}</a></p>
    </div>
  </section>
</template>

<script>
// import QuestionCard from './QuestionCard.vue'

export default {
  name: 'QuestionDetail',
  components: {
    // QuestionCard,
  },

  data() {
    return {
      question: null,
      answerPicked: '',
      questionSubmitted: false,
      questionSuccess: false,
      loading: false,
      error: null,
    }
  },

  created () {
    if (this.$route.params.question) {
      this.question = this.$route.params.question;
    } else {
      this.fetchQuestion();
    }
  },
  methods: {
    fetchQuestion() {
      this.error = this.question = null;
      this.loading = true;
      fetch(`http://localhost:8000/api/questions/${this.$route.params.questionId}`)
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
}
</style>