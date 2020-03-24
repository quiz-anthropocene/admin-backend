<template>
  <section>
    <br />

    <div v-if="loading" class="loading">
      Chargement de la question...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="question" class="question">
      <h2>
        <span>
          <span class="hidden-sm">Question&nbsp;</span>
          <span class="color-blue">#{{ question.id }}</span>
        </span>
        <span> | </span>
        <span class="color-orange">{{ question.category }}</span>
        <span> | </span>
        <span><small><DifficultyBadge v-bind:difficulty="question.difficulty" /></small></span>
      </h2>
      <h3>{{ question.text }}</h3>
      <form @submit.prevent="submitQuestion">
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

    <div v-if="question && questionSubmitted" class="answer">
      <h2 v-if="questionSuccess">{{ questionSuccess }} !</h2>
      <h2 v-if="!questionSuccess">Pas tout à fait...</h2>
      <h3 v-if="!questionSuccess">La réponse était: {{ question["answer_option_" + question["answer_correct"]] }}</h3>
      <p title="Explication">
        ℹ️&nbsp;{{ question.answer_explanation }}
      </p>
      <p title="Lien(s) pour aller plus loin">
        🔗&nbsp;<a v-bind:href="question.answer_additional_links" target="_blank">{{ question.answer_additional_links }}</a>
      </p>
      <p v-if="question.answer_image_link" class="answer-image" title="Une image pour illustrer la réponse">
        🖼️&nbsp;<small>(cliquez sur l'image pour l'agrandir)</small><br />
        <a v-bind:href="question.answer_image_link" target="_blank"><img v-bind:src="question.answer_image_link" alt="une image pour illustrer la réponse" /></a>
      </p>
      <hr class="custom-seperator" />
      <div class="row margin-top-bottom-10 small">
        <div title="Auteur de la question">📝&nbsp;Auteur:&nbsp;{{ question.author }}</div>
        <div title="Statistiques de la question">📊&nbsp;Stats:&nbsp;{{ question.answer_success_count }} / {{ question.answer_count }} ({{ question.answer_success_rate }}%)</div>
      </div>
    </div>

    <div v-if="question" class="action small">
      <br />
      <router-link :to="{ name: 'question-detail', params: { questionId: questionSameCategoryNextId } }">
        <button class="button">⏩&nbsp;Autre question <span class="color-orange">{{ question.category }}</span></button>
      </router-link>
      <router-link :to="{ name: 'question-detail', params: { questionId: questionRandomNextId } }">
        <button class="button">🔀&nbsp;Question au hasard</button>
      </router-link>
    </div>

    <HomeLink v-if="question" />
  </section>
</template>

<script>
// import QuestionCard from './QuestionCard.vue'
import DifficultyBadge from './DifficultyBadge.vue'
import HomeLink from './HomeLink.vue'

export default {
  name: 'QuestionDetail',
  components: {
    // QuestionCard,
    DifficultyBadge,
    HomeLink,
  },

  data() {
    return {
      question: null,
      answerPicked: '',
      questionSubmitted: false,
      questionSuccess: null,
      questionSuccessMessageList: ["C'est exact", "En effet", "Bien vu", "Félicitations", "Bravo"],
      questionSameCategoryNextId: null,
      questionRandomNextId: null,
      loading: false,
      error: null,
    }
  },

  created () {
    this.init(this.$route.params.questionId);
  },

  beforeRouteUpdate (to, from, next) {
    this.init(to.params.questionId);
    next();
  },

  methods: {
    init(currentQuestionId) {
      this.answerPicked = '';
      this.questionSubmitted = false;
      this.questionSuccess = null;
      this.loading = false;
      this.error = null;
      this.fetchQuestion(currentQuestionId);
    },
    fetchQuestion(questionId) {
      this.error = this.question = null;
      this.loading = true;
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/questions/${questionId}`)
        .then(response => {
          this.loading = false
          return response.json()
        })
        .then(data => {
          this.question = data;
          this.fetchQuestionRandomNext(this.question.id, this.question.category);
          this.fetchQuestionRandomNext(this.question.id);
        })
        .catch(error => {
          console.log(error)
          this.error = error;
        })
    },
    fetchQuestionRandomNext(currentQuestionId, currentQuestionCategory = null) {
      const params = { 'current': currentQuestionId };
      if (currentQuestionCategory) {
        params['category'] = currentQuestionCategory;
      }
      const urlParams = new URLSearchParams(Object.entries(params));
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/questions/random?${urlParams}`)
        .then(response => {
          this.loading = false
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
          this.error = error;
        })
    },
    submitQuestion() {
      this.questionSubmitted = true;
      // TODO: validate answer in the backend
      this.questionSuccess = (this.answerPicked === this.question.answer_correct) ? this.questionSuccessMessageList[Math.floor(Math.random() * this.questionSuccessMessageList.length)] : null;
      // TODO: increment question stats in the backend
      this.question.answer_count += 1;
      this.question.answer_success_count += (this.questionSuccess ? 1 : 0);
      this.question.answer_success_rate = ((this.question.answer_success_count / this.question.answer_count) * 100).toFixed(0);
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/questions/${this.$route.params.questionId}/stats`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ answer_choice: this.answerPicked })
      })
        .then(response => {
          this.loading = false
          return response.json()
        })
        .then(data => {
          console.log(data);
        })
        .catch(error => {
          console.log(error)
        })
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
  overflow: hidden;
}
.answer p.answer-image {
  height: 300px;
}
.answer p.answer-image img {
  max-height: 90%;
  max-width: 100%;
  margin: auto;
}
</style>