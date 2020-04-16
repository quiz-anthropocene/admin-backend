<template>
  <section>
    <div v-if="question" class="question">
      <h2>
        <span>
          <!-- <span class="d-none d-sm-inline">Question&nbsp;</span> -->
          <span class="text-primary">#{{ context.question_number }}</span>
        </span>
        <span> | </span>
        <span class="text-secondary">{{ question.category }}</span>
        <span> | </span>
        <span><small><DifficultyBadge v-bind:difficulty="question.difficulty" /></small></span>
      </h2>
      <h3>{{ question.text }}</h3>
      <form @submit.prevent="submitAnswer">
        <div v-for="answer_option_letter in answerChoices" :key="answer_option_letter" :class="{ 'text-primary' : answerPicked === answer_option_letter }">
          <template v-if="question['answer_option_' + answer_option_letter]">
            <input type="radio" v-bind:id="answer_option_letter" v-bind:value="answer_option_letter" v-model="answerPicked" :disabled="questionSubmitted">&nbsp;
            <label v-bind:for="answer_option_letter">&nbsp;{{ question['answer_option_' + answer_option_letter] }}</label>
          </template>
        </div>
        <div>
          <button v-if="!questionSubmitted" type="submit" class="btn btn-outline-primary" :disabled="!answerPicked">Valider</button>
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
        <div v-if="question.tags && question.tags.length > 0" title="Tag(s) de la question">🏷️&nbsp;Tag<span v-if="question.tags.length > 1">s</span>:&nbsp;{{ question.tags.join(', ') }}</div>
        <div title="Auteur de la question">📝&nbsp;Auteur:&nbsp;{{ question.author }}</div>
        <div title="Statistiques de la question">📊&nbsp;Stats:&nbsp;{{ question.answer_success_count }} / {{ question.answer_count }} ({{ question.answer_success_rate }}%)</div>
      </div>
    </div>
  </section>
</template>

<script>
import DifficultyBadge from '../components/DifficultyBadge.vue'

export default {
  name: 'QuestionAnswerCards',
  props: {
    question: Object,
    context: Object
  },
  components: {
    DifficultyBadge
  },

  data() {
    return {
      // question: null,
      answerChoices: [],
      answerPicked: '',
      questionSubmitted: false,
      questionSuccess: null,
      questionSuccessMessageList: ["C'est exact", "En effet", "Bien vu", "Félicitations", "Bravo"],
    }
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
      this.answerChoices = this.shuffleAnswers(['a', 'b', 'c', 'd'], this.question.has_ordered_answers);
      this.answerPicked = '';
      this.questionSubmitted = false;
      this.questionSuccess = null;
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
    submitAnswer() {
      this.questionSubmitted = true;
      // TODO: validate answer in the backend
      this.questionSuccess = (this.answerPicked === this.question.answer_correct) ? this.questionSuccessMessageList[Math.floor(Math.random() * this.questionSuccessMessageList.length)] : null;
      // TODO: increment question stats in the backend
      this.question.answer_count += 1;
      this.question.answer_success_count += (this.questionSuccess ? 1 : 0);
      this.question.answer_success_rate = ((this.question.answer_success_count / this.question.answer_count) * 100).toFixed(0);
      // tell parent component
      this.$emit('answerSubmitted', { question_id: this.question.id, success: this.questionSuccess });
      // stats
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/questions/${this.question.id}/stats`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          answer_choice: this.answerPicked,
          source: this.context.source
        })
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
