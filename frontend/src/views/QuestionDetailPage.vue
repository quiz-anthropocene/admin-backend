<template>
  <section>
    <br />

    <div v-if="question" class="question">
      <h2>
        <span>
          <span class="d-none d-sm-inline">Question&nbsp;</span>
          <span class="text-primary">#{{ question.id }}</span>
        </span>
        <span> | </span>
        <span class="text-secondary">{{ question.category }}</span>
        <span> | </span>
        <span><small><DifficultyBadge v-bind:difficulty="question.difficulty" /></small></span>
      </h2>
      <h3>{{ question.text }}</h3>
      <form @submit.prevent="submitQuestion">
        <div v-for="answer_option_letter in answerChoices" :key="answer_option_letter" :class="{ 'text-primary' : answerPicked === answer_option_letter }">
          <template v-if="question['answer_option_' + answer_option_letter]">
            <input type="radio" v-bind:id="answer_option_letter" v-bind:value="answer_option_letter" v-model="answerPicked" :disabled="questionSubmitted">&nbsp;
            <label v-bind:for="answer_option_letter">&nbsp;{{ question['answer_option_' + answer_option_letter] }}</label>
          </template>
        </div>
        <div>
          <button type="submit" class="btn btn-outline-primary" :disabled="questionSubmitted || !answerPicked">Valider</button>
        </div>
      </form>
    </div>

    <br v-if="question && questionSubmitted" />

    <div v-if="question && questionSubmitted" class="answer" :class="questionSuccess ? 'answer-success' : 'answer-error'">
      <h2 v-if="questionSuccess">{{ questionSuccess }} !</h2>
      <h2 v-if="!questionSuccess">Pas tout à fait...</h2>
      <h3 v-if="!questionSuccess">La réponse était: {{ question["answer_option_" + question["answer_correct"]] }}</h3>
      <p title="Explication">
        ℹ️&nbsp;{{ question.answer_explanation }}
      </p>
      <p title="Lien(s) pour aller plus loin">
        🔗&nbsp;<a v-bind:href="question.answer_additional_link" target="_blank">{{ question.answer_additional_link }}</a>
      </p>
      <p v-if="question.answer_image_link" class="answer-image" title="Une image pour illustrer la réponse">
        <a v-bind:href="question.answer_image_link" target="_blank">
          <img v-bind:src="question.answer_image_link" alt="une image pour illustrer la réponse" />
        </a>
      </p>
      <hr class="custom-seperator" />
      <div class="row margin-top-bottom-10 small">
        <div v-if="question.tags" title="Tag(s) de la question">🏷️&nbsp;Tag<span v-if="question.tags.length > 1">s</span>:&nbsp;{{ question.tags.join(', ') }}</div>
        <div title="Auteur de la question">📝&nbsp;Auteur:&nbsp;{{ question.author }}</div>
        <div title="Statistiques de la question">📊&nbsp;Stats:&nbsp;{{ question.answer_success_count }} / {{ question.answer_count }} ({{ question.answer_success_rate }}%)</div>
      </div>
    </div>

    <div v-if="question" class="small">
      <br />
      <router-link :to="{ name: 'question-detail', params: { questionId: questionSameCategoryNextId } }">
        <button class="btn btn-outline-primary">⏩&nbsp;Autre question <span class="text-secondary">{{ question.category }}</span></button>
      </router-link>
      <router-link :to="{ name: 'question-detail', params: { questionId: questionRandomNextId } }">
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
// import QuestionCard from '../components/QuestionCard.vue'
import DifficultyBadge from '../components/DifficultyBadge.vue'
import HomeLink from '../components/HomeLink.vue'

export default {
  name: 'Page',
  components: {
    // QuestionCard,
    DifficultyBadge,
    HomeLink,
  },

  data() {
    return {
      // question: null,
      answerChoices: [],
      answerPicked: '',
      questionSubmitted: false,
      questionSuccess: null,
      questionSuccessMessageList: ["C'est exact", "En effet", "Bien vu", "Félicitations", "Bravo"],
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
          this.initQuestion();
        }
      }
    }
  },

  mounted () {
  },

  methods: {
    initQuestion() {
      console.log("initQuestion")
      this.answerChoices = this.shuffleAnswers(['a', 'b', 'c', 'd'], this.question.has_ordered_answers);
      this.answerPicked = '';
      this.questionSubmitted = false;
      this.questionSuccess = null;
      this.fetchQuestionRandomNext(this.question.id, this.question.category);
      this.fetchQuestionRandomNext(this.question.id);
    },
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
    shuffleAnswers(answers_array, has_ordered_answers) {
      if (has_ordered_answers) {
        return answers_array;
      } else {
        // https://medium.com/@nitinpatel_20236/how-to-shuffle-correctly-shuffle-an-array-in-javascript-15ea3f84bfb
        for (let i = answers_array.length-1; i > 0; i--) {
          const j = Math.round(Math.random() * i);
          const temp = answers_array[i];
          answers_array[i] = answers_array[j];
          answers_array[j] = temp;
        }
        return answers_array;
      }
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
