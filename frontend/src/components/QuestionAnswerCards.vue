<template>
  <section>

    <!-- Question -->
    <div v-if="question" class="question">
      <h2>
        <span>
          <span class="text-primary">#{{ context.question_number }}</span>
        </span>
        <span> | </span>
        <span class="text-secondary">{{ question.category.name }}</span>
        <span> | </span>
        <span><small><DifficultyBadge v-bind:difficulty="question.difficulty" /></small></span>
      </h2>
      <form @submit.prevent="submitAnswer">
        <!-- Question text -->
        <div class="row no-gutters justify-content-center">
          <div class="col-md-10 col-lg-8">
            <h3 v-html="$options.filters.abbr(questionTextWithLineBreaks, glossaire)"></h3>
          </div>
        </div>
        <!-- Question answer choices -->
        <div v-if="question.type !== 'QCM-RM'" class="row justify-content-center">
          <div class="col-sm-auto text-align-left">
            <div class="form-group" v-for="answer_option_letter in answerChoices" :key="answer_option_letter" :class="{ 'text-primary' : answer_option_letter === answerPicked, 'text-danger': (questionSubmitted && (answer_option_letter !== answerPicked) && (answer_option_letter === question['answer_correct'])) }">
              <template v-if="question['answer_option_' + answer_option_letter]">
                <input type="radio" v-bind:id="answer_option_letter" v-bind:value="answer_option_letter" v-model="answerPicked" :disabled="questionSubmitted">&nbsp;
                <label v-bind:for="answer_option_letter">&nbsp;{{ question['answer_option_' + answer_option_letter] }}</label>
              </template>
            </div>
          </div>
        </div>
        <div v-if="question.type === 'QCM-RM'" class="row justify-content-center">
          <div class="col-12 margin-bottom-10"><i>⚠️&nbsp;plusieurs réponses possibles</i></div>
          <div class="col-sm-auto text-align-left">
            <div class="form-group" v-for="(answer_option_letter, index) in answerChoices" :key="answer_option_letter" :class="{ 'text-primary' : answerPicked.includes(answer_option_letter), 'text-warning': (questionSubmitted && answerPicked.includes(answer_option_letter) && !question['answer_correct'].includes(answer_option_letter)), 'text-danger': (questionSubmitted && !answerPicked.includes(answer_option_letter) && question['answer_correct'].includes(answer_option_letter)) }">
              <template v-if="question['answer_option_' + answer_option_letter]">
                <input type="checkbox" v-bind:id="answer_option_letter" v-bind:value="answer_option_letter" v-model="answerPicked[index]" v-bind:true-value="answer_option_letter" :disabled="questionSubmitted">&nbsp;
                <label v-bind:for="answer_option_letter">&nbsp;{{ question['answer_option_' + answer_option_letter] }}</label>
              </template>
            </div>
          </div>
        </div>
        <!-- Question hint & form submit -->
        <div v-if="question.hint && showQuestionHint" class="row no-gutters justify-content-center">
          <div class="col-md-10 col-lg-8">
            <div class="alert alert-warning-custom text-align-left margin-bottom-10 padding-10">💡{{ question.hint }}</div>
          </div>
        </div>
        <div class="row no-gutters">
          <div class="col-4">
            <button v-if="question.hint && !showQuestionHint" class="btn btn-sm btn-outline-warning" @click="showQuestionHint=!showQuestionHint">💡un indice</button>
          </div>
          <div class="col-4">
            <div class="form-group">
              <button v-if="!questionSubmitted" type="submit" class="btn" :class="answerPicked ? 'btn-primary' : 'btn-outline-primary'" :disabled="!answerPicked">Valider</button>
            </div>
          </div>
          <div class="col-4"></div>
        </div>
      </form>
    </div>

    <!-- <br v-if="question && questionSubmitted" /> -->
    <div v-if="question && questionSubmitted" id="scroll-to-answer" style="height:1px"></div>

    <!-- Answer -->
    <div v-if="question && questionSubmitted" class="answer" :class="questionSuccess ? 'answer-success' : 'answer-error'">
      <h2 v-if="questionSuccess">{{ questionSuccess }} !</h2>
      <h2 v-if="!questionSuccess">Pas tout à fait...</h2>
      <h3 v-if="!questionSuccess">La réponse était: {{ question["answer_option_" + question["answer_correct"]] }}</h3>
      <div class="row no-gutters text-align-left">
        <div class="col-sm-auto">
          <p title="Explication">
            <span>ℹ️&nbsp;</span>
            <span v-html="$options.filters.abbr(questionAnswerExplanationWithLineBreaks, glossaire)"></span>
          </p>
        </div>
      </div>
      <div class="row no-gutters text-align-left">
        <div class="col-sm-auto">
          <p class="answer-link" v-if="question.answer_accessible_url" title="Lien accessible pour aller plus loin">
            🔗&nbsp;<a v-bind:href="question.answer_accessible_url" target="_blank" v-bind:title="question.answer_accessible_url">{{ question.answer_accessible_url }}</a>
          </p>
          <p class="answer-link" v-if="question.answer_scientific_url" title="Lien scientifique pour creuser la source">
            🔗🧬&nbsp;<a v-bind:href="question.answer_scientific_url" target="_blank" v-bind:title="question.answer_scientific_url">{{ question.answer_scientific_url }}</a>
          </p>
        </div>
      </div>
      <p v-if="question.answer_image_url" class="answer-image" title="Une image pour illustrer la réponse">
        <a v-bind:href="question.answer_image_url" target="_blank">
          <img v-bind:src="question.answer_image_url" alt="une image pour illustrer la réponse" />
        </a>
      </p>
      <p v-if="question.answer_image_explanation" class="answer-image-explanation" title="Légende de l'image">Légende: {{ question.answer_image_explanation }}</p>

      <!-- <div class="separator-with-text"></div> -->
      <hr class="margin-top-bottom-10" />

      <!-- Extra info -->
      <div class="row no-gutters small">
        <div class="col-sm" title="Auteur de la question">
          📝&nbsp;Auteur<span class="label label-hidden"><strong>{{ question.author }}</strong></span>
        </div>
        <div class="col-sm" v-if="question.tags && question.tags.length > 0" title="Tag(s) de la question">
          <!-- 🏷️&nbsp;Tag<span v-if="question.tags.length > 1">s</span>:&nbsp;{{ question.tags.map(t => t.name).join(', ') }} -->
          🏷️&nbsp;<span v-for="tag in question.tags" :key="tag.id">
            <span class="label label-tag">{{ tag.name }}</span>
          </span>
        </div>
        <!-- <div title="Statistiques de la question">📊&nbsp;Stats:&nbsp;{{ question.answer_success_count_agg }} / {{ question.answer_count_agg }} ({{ question.answer_success_rate }}%)</div> -->
      </div>

    </div>

    <FeedbackCard v-if="question && questionSubmitted" v-bind:context="{ source: 'question', item: question }" />
  </section>
</template>

<script>
import constants from '../constants';
import DifficultyBadge from './DifficultyBadge.vue';
import FeedbackCard from './FeedbackCard.vue';

export default {
  name: 'QuestionAnswerCards',
  props: {
    question: Object,
    context: Object,
  },
  components: {
    DifficultyBadge,
    FeedbackCard,
  },

  data() {
    return {
      // question: null,
      showQuestionHint: false,
      answerChoices: [],
      answerPicked: null,
      questionSubmitted: false,
      questionSuccess: null,
      questionSuccessMessageList: constants.QUESTION_SUCCESS_MESSAGES,
    };
  },

  computed: {
    glossaire() {
      return this.$store.state.ressources.glossaire;
    },
    questionTextWithLineBreaks() {
      return this.question.text.replace(/(?:\r\n|\r|\n)/g, '<br />');
    },
    questionAnswerExplanationWithLineBreaks() {
      return this.question.answer_explanation.replace(/(?:\r\n|\r|\n)/g, '<br />');
    },
  },

  watch: {
    question: {
      immediate: true,
      // eslint-disable-next-line
      handler(newQuestion, oldQuestion) {
        if (newQuestion) {
          this.initQuestion();
          this.initContribution();
        }
      },
    },
  },

  mounted() {
    if (this.$route.query.showdetails) {
      this.questionSubmitted = true;
    }
  },

  methods: {
    initQuestion() {
      this.showQuestionHint = false;
      this.answerChoices = this.shuffleAnswers(['a', 'b', 'c', 'd'], this.question.has_ordered_answers);
      this.answerPicked = (this.question.type === 'QCM-RM') ? new Array(this.question.answer_correct.length).fill('') : '';
      this.questionSubmitted = false;
      this.questionSuccess = null;
      // this.feedbackSubmitted = false;
    },
    initContribution() {
      this.contribution = {
        text: '',
        description: `Question #${this.question.id} - ${this.question.category.name} - ${this.question.text}`,
        type: 'commentaire question',
      };
      this.showContributionForm = false;
      this.contributionSubmitted = false;
      this.contributionResponse = null;
      this.loading = false;
      this.error = null;
    },
    shuffleAnswers(answersArray, hasOrderedAnswers) {
      if (hasOrderedAnswers) {
        return answersArray;
      }
      // https://medium.com/@nitinpatel_20236/how-to-shuffle-correctly-shuffle-an-array-in-javascript-15ea3f84bfb
      for (let i = answersArray.length - 1; i > 0; i--) {
        const j = Math.round(Math.random() * i);
        const temp = answersArray[i];
        answersArray[i] = answersArray[j];
        answersArray[j] = temp;
      }
      return answersArray;
    },
    submitAnswer() {
      // init
      this.questionSubmitted = true;
      const cleanedAnswerPicked = (this.question.type === 'QCM-RM') ? this.answerPicked.slice(0).filter(Boolean).sort().join('') : this.answerPicked;
      const randomSuccessMessage = this.questionSuccessMessageList[Math.floor(Math.random() * this.questionSuccessMessageList.length)];
      // validate answer
      this.questionSuccess = (cleanedAnswerPicked === this.question.answer_correct) ? randomSuccessMessage : null;
      // update question stats // watch out for eslint 'vue/no-mutating-props'
      // this.question.answer_count_agg += 1;
      // this.question.answer_success_count_agg += (this.questionSuccess ? 1 : 0);
      // this.question.answer_success_rate = ((this.question.answer_success_count_agg / this.question.answer_count_agg) * 100).toFixed(0);
      // tell parent component
      this.$emit('answer-submitted', { question_id: this.question.id, success: this.questionSuccess });
      // scroll to answer
      setTimeout(() => {
        // why scroll to this div and not to 'answer' directly ? To have a slight top margin
        // document.getElementsByClassName('answer')[0].scrollIntoView({ behavior: 'smooth' });
        document.getElementById('scroll-to-answer').scrollIntoView({ behavior: 'smooth' });
      }, 25);
      // stats
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/questions/${this.question.id}/answer-events`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          choice: cleanedAnswerPicked,
          source: this.context.source,
        }),
      })
        .then((response) => response.json())
      // eslint-disable-next-line
      .then(data => {
        // console.log(data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>
.question {
  border: 2px solid var(--primary);
  border-radius: 5px;
  margin: 10px 0px;
  padding: 10px;
  background-color: white;
}

/* hint */
.alert-warning-custom {
  color: var(--primary);
  background-color: inherit;
  border-color: var(--warning);
}
button.btn-outline-warning {
  color: var(--primary);
  margin-top: 4px; /* vertical center with submit button */
}

.answer {
  border: 2px solid;
  border-radius: 5px;
  margin: 10px 0px;
  scroll-margin: 10px;
  padding: 10px;
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
.answer p.answer-link {
  white-space: nowrap;
  overflow-x: hidden;
  text-overflow: ellipsis;
}
.answer p.answer-image {
  height: 300px;
}
.answer p.answer-image img {
  background-color: white;
  max-height: 100%;
  max-width: 100%;
  margin: auto;
}
.answer-image-explanation {
  font-style: italic;
  font-size: small;
}

@media all and (min-width: 60em) {
  .answer p.answer-image {
    height: 500px;
  }
}
</style>
