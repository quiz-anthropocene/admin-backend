<template>
  <section>

    <!-- QUESTION -->
    <div v-if="question" class="question">
      <form @submit.prevent="submitAnswer">
        <!-- Question text -->
        <div class="row no-gutters justify-content-center margin-bottom-10">
          <div class="col-md-10 col-lg-8">
            <h3 v-html="$options.filters.abbr(questionTextWithLineBreaks, glossaire)"></h3>
          </div>
        </div>

        <!-- Question answer choices -->
        <div v-if="question.type !== 'QCM-RM'" class="row justify-content-center margin-bottom-10">
          <div class="col-sm-auto col-md-8 col-lg-6 text-align-left">
            <div class="form-group" v-for="answer_option_letter in answerChoices" :key="answer_option_letter" :class="{ 'text-primary' : answer_option_letter === answerPicked, 'text-danger': (questionSubmitted && (answer_option_letter !== answerPicked) && (answer_option_letter === question['answer_correct'])) }">
              <label v-if="question['answer_option_' + answer_option_letter]" :for="answer_option_letter">
                <input type="radio" v-bind:id="answer_option_letter" v-bind:value="answer_option_letter" v-model="answerPicked" :disabled="questionSubmitted">&nbsp;
                {{ question['answer_option_' + answer_option_letter] }}
              </label>
            </div>
          </div>
        </div>
        <div v-if="question.type === 'QCM-RM'" class="row justify-content-center margin-bottom-10">
          <div class="col-12 margin-bottom-10 small"><i>{{ $t('messages.multipleAnswers') }}</i></div>
          <div class="col-sm-auto col-md-8 col-lg-6 text-align-left">
            <div class="form-group" v-for="(answer_option_letter, index) in answerChoices" :key="answer_option_letter" :class="{ 'text-primary' : answerPicked.includes(answer_option_letter), 'text-warning': (questionSubmitted && answerPicked.includes(answer_option_letter) && !question['answer_correct'].includes(answer_option_letter)), 'text-danger': (questionSubmitted && !answerPicked.includes(answer_option_letter) && question['answer_correct'].includes(answer_option_letter)) }">
              <label v-if="question['answer_option_' + answer_option_letter]" :for="answer_option_letter">
                <input type="checkbox" v-bind:id="answer_option_letter" v-bind:value="answer_option_letter" v-model="answerPicked[index]" v-bind:true-value="answer_option_letter" :disabled="questionSubmitted">&nbsp;
                {{ question['answer_option_' + answer_option_letter] }}
              </label>
            </div>
          </div>
        </div>

        <!-- Question hint -->
        <div v-if="question.hint && showQuestionHint" class="row no-gutters justify-content-center margin-bottom-10">
          <div class="col-md-10 col-lg-8">
            <div class="alert alert-warning-custom text-align-left margin-bottom-10 padding-10">💡{{ question.hint }}</div>
          </div>
        </div>

        <!-- Question form submit -->
        <div class="row no-gutters">
          <div class="col-4">
            <span class="text-primary">#{{ context.question_number }}</span><br />
            <span><small><DifficultyBadge v-bind:difficulty="question.difficulty" /></small></span>
          </div>
          <div class="col-4">
            <button v-if="!questionSubmitted" type="submit" class="btn" :class="answerPicked ? 'btn-primary' : 'btn-outline-primary'" :disabled="!answerPicked">{{ $t('messages.submit') }}</button>
          </div>
          <div class="col-4">
            <button v-if="question.hint && !showQuestionHint" class="btn btn-sm btn-outline-warning" @click="showQuestionHint=!showQuestionHint">💡&nbsp;{{ $t('messages.hint') }}</button>
          </div>
        </div>
      </form>
    </div>

    <!-- <br v-if="question && questionSubmitted" /> -->
    <div v-if="question && questionSubmitted" id="scroll-to-answer" class="scroll-to-fix" style="height:0px"></div>

    <!-- ANSWER -->
    <div v-if="question && questionSubmitted" class="answer" :class="questionAnswer.success ? 'answer-success' : 'answer-error'">
      <!-- Good answer -->
      <h2 v-if="questionAnswer.success">{{ questionAnswer.message }}</h2>
      <!-- Wrong answer -->
      <h2 v-if="!questionAnswer.success">{{ questionAnswer.message }}</h2>
      <h3 v-if="!questionAnswer.success">
        <small>{{ $t('messages.answerWas') }}{{ $t('words.semiColon') }}&nbsp;</small>
        <span v-if="question.type !== 'QCM-RM'">{{ question["answer_option_" + question["answer_correct"]] }}</span>
        <ul v-if="question.type === 'QCM-RM'">
          <li v-for="answer_correct_letter in question['answer_correct']" :key="answer_correct_letter">
            <span>{{ question["answer_option_" + answer_correct_letter] }}</span>
          </li>
        </ul>
      </h3>
      <!-- Answer explanation -->
      <div class="row no-gutters text-align-left">
        <div class="col-sm-auto">
          <p title="Explication">
            <span>ℹ️&nbsp;</span>
            <span v-html="$options.filters.abbr(questionAnswerExplanationWithLineBreaks, glossaire)"></span>
          </p>
          <p v-if="question.answer_audio" title="Explication au format audio">
            <span>🔈&nbsp;</span>
            <audio controls>
              <source v-bind:src="question.answer_audio" type="audio/mpeg">
              Votre navigateur ne supporte par le HTML5 audio. Voici un <a href="question.answer_audio">lien pour télécharger le fichier audio</a>.
            </audio>
          </p>
          <p v-if="question.answer_video" title="Explication au format vidéo">
            <span>📺&nbsp;</span>
            <video v-if="question.answer_video.endsWith('.mp4')" controls height="250" type="video/mp4">
              <source v-bind:src="question.answer_video">
              Votre navigateur ne supporte par le HTML5 vidéo. Voici un <a href="question.answer_video">lien pour télécharger le fichier vidéo</a>.
            </video>
            <!-- <object v-if="!question.answer_video.endsWith('.mp4')" :data="question.answer_video" height="250"></object> -->
            <a v-bind:href="question.answer_video" target="_blank">{{ question.answer_video }}</a>
          </p>
        </div>
      </div>
      <!-- Answer image -->
      <p v-if="question.answer_image_url" class="answer-image" title="Une image pour illustrer la réponse">
        <a v-bind:href="question.answer_image_url" target="_blank">
          <img v-bind:src="question.answer_image_url" alt="Une image pour illustrer la réponse" />
        </a>
      </p>
      <p v-if="question.answer_image_explanation" class="answer-image-explanation" title="Légende de l'image">{{ $t('messages.imageLegend') }}{{ $t('words.semiColon') }} {{ question.answer_image_explanation }}</p>
      <!-- Answer links -->
      <div class="row no-gutters text-align-left">
        <div class="col-sm-auto">
          <p class="answer-link" v-if="question.answer_accessible_url" title="Lien accessible pour aller plus loin">
            🔗&nbsp;<a v-bind:href="question.answer_accessible_url" target="_blank" v-bind:title="question.answer_accessible_url">{{ question.answer_accessible_url_text ? question.answer_accessible_url_text : question.answer_accessible_url }}</a>
          </p>
          <p class="answer-link" v-if="question.answer_scientific_url" title="Lien scientifique pour creuser la source">
            🔗🧬&nbsp;<a v-bind:href="question.answer_scientific_url" target="_blank" v-bind:title="question.answer_scientific_url">{{ question.answer_scientific_url_text ? question.answer_scientific_url_text : question.answer_scientific_url }}</a>
          </p>
          <p v-if="question.answer_reading_recommendation" title="Un livre pour aller plus loin">
            📚&nbsp;{{ question.answer_reading_recommendation }}
          </p>
        </div>
      </div>
    </div>

    <div v-if="question && questionSubmitted && questionNotValidated" class="alert alert-warning">
      {{ $t('messages.questionPendingValidation') }}
    </div>

    <FeedbackCard v-if="question && questionSubmitted" v-bind:context="{ source: 'question', item: question, quiz: context.quiz }" />
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
      questionSuccessMessageList: (this.$i18n.locale !== 'fr') ? constants.QUESTION_SUCCESS_MESSAGES_EN : constants.QUESTION_SUCCESS_MESSAGES_FR,
      questionErrorAlmostMessageList: (this.$i18n.locale !== 'fr') ? constants.QUESTION_ERROR_ALMOST_MESSAGES_EN : constants.QUESTION_ERROR_ALMOST_MESSAGES_FR,
      questionErrorMessageList: (this.$i18n.locale !== 'fr') ? constants.QUESTION_ERROR_MESSAGES_EN : constants.QUESTION_ERROR_MESSAGES_FR,
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
    questionNotValidated() {
      return this.question.validation_status !== constants.QUESTION_VALIDATION_STATUS_OK;
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
  },

  methods: {
    initQuestion() {
      this.showQuestionHint = false;
      this.answerChoices = this.shuffleAnswers(['a', 'b', 'c', 'd'], this.question.has_ordered_answers);
      this.answerPicked = (this.question.type === 'QCM-RM') ? new Array(this.question.answer_correct.length).fill('') : '';
      this.questionSubmitted = false;
      this.questionAnswer = {};
      // this.feedbackSubmitted = false;
    },
    initContribution() {
      this.contribution = {
        text: '',
        description: `Question #${this.question.id} - ${this.question.text}`,
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
      const randomErrorMessage = this.questionErrorMessageList[Math.floor(Math.random() * this.questionErrorMessageList.length)];
      const randomErrorAlmostMessage = this.questionErrorAlmostMessageList[Math.floor(Math.random() * this.questionErrorAlmostMessageList.length)];
      // validate answer
      this.questionAnswer.success = (cleanedAnswerPicked === this.question.answer_correct);
      this.questionAnswer.message = this.questionAnswer.success ? randomSuccessMessage : ((this.question.type === 'QCM-RM') ? randomErrorAlmostMessage : randomErrorMessage);
      // update question stats // watch out for eslint 'vue/no-mutating-props'
      // this.question.answer_count_agg += 1;
      // this.question.answer_success_count_agg += (this.questionSuccess ? 1 : 0);
      // this.question.answer_success_rate = ((this.question.answer_success_count_agg / this.question.answer_count_agg) * 100).toFixed(0);
      // tell parent component
      this.$emit('answer-submitted', {
        question_id: this.question.id,
        success: this.questionAnswer.success,
        answer_correct: this.question.answer_correct,
        answer_picked: cleanedAnswerPicked,
        message: this.questionAnswer.message
        });
      // scroll to answer
      setTimeout(() => {
        // why scroll to this div and not to 'answer' directly ? To have a slight top margin
        document.getElementById('scroll-to-answer').scrollIntoView({ behavior: 'smooth' });
      }, 25);
      // stats
      fetch(`${process.env.VUE_APP_STATS_ENDPOINT}/question-answer-event/`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: this.question.id,
          choice: cleanedAnswerPicked,
          source: this.context.source,
          quiz: this.context.quiz ? this.context.quiz.id : null
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
.question .form-group label {
  display: block;
  box-sizing: border-box;
  box-shadow: 0px 0px 2px 2px #ededed;
  border-radius: 5px;
  padding: 5px 10px;
  margin-bottom: 0;
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
