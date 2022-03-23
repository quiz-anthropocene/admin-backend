<template>
  <section>

    <section v-if="!quiz">
      <div class="alert alert-warning" role="alert">
        {{ $t('messages.quizNotFound') }}
      </div>
      <router-link class="no-decoration" :to="{ name: 'quiz-list' }">
        <button id="all-quizs-btn" class="btn btn-primary btn-lg">
          🕹&nbsp;<strong>{{ $t('messages.allQuizs') }}</strong>
        </button>
      </router-link>
    </section>

    <section v-if="quiz && quiz.language !== currentLocale.value" class="alert alert-warning" role="alert">
      {{ $t('messages.quizOtherLanguage') }}
    </section>

    <!-- Quiz header -->
    <div v-if="quiz" class="card">
      <img v-bind:src="quiz.image_background_url || 'https://quizanthropocene.fr/showyourstripes_globe_1850-2019.png'" class="card-img-top" :class="(quizStep === 0) ? 'height-150' : 'height-50'">

      <div class="card-body">
        <h2 class="card-title">
          Quiz{{ $t('words.semiColon') }} {{ quiz.name }}
          <span v-if="quiz.has_audio" class="label small" style="vertical-align:top">🔉{{ $t('messages.audioComments') }}</span>
        </h2>

        <section v-if="(quizStep === 0) || (quizStep > quiz.questions.length)">
          <div class="row no-gutters justify-content-center card-subtitle">
            <div class="col-md-10 col-lg-8" v-html="quiz.introduction" title="Introduction du quiz"></div>
          </div>

          <hr class="margin-top-bottom-10" />

          <div class="row no-gutters small">
            <div class="col" title="Nombre de questions">
              <span class="label label-hidden"><strong>{{ quiz.questions.length }}</strong></span>Questions
            </div>
            <!-- <div class="col" v-bind:title="$t('messages.difficulty')">
              🏆&nbsp;{{ $t('messages.difficulty') }}<span class="label label-hidden"><strong>{{ quiz.difficulty_average | round(1) }} / 4</strong></span>
            </div> -->
            <div class="col" title="Auteur du quiz">
              📝&nbsp;{{ $t('messages.author') }}<span class="label label-hidden"><strong>{{ quiz.author }}</strong></span>
            </div>
            <!-- <span title="Date de création du quiz">📊&nbsp;Crée le:&nbsp;{{ new Date(quiz.created).toLocaleString() }}</span> -->
            <div v-if="quiz.tags && quiz.tags.length > 0" class="col small d-none d-sm-block" title="Mot(s) clé(s) du quiz">
              <span v-for="(tag, index) in quiz.tags" :key="tag.id">
                <span v-if="index < 3" class="label label-tag">{{ tag.name }}</span>
              </span>
            </div>
          </div>

          <hr v-if="previousQuiz" class="margin-top-bottom-10" />

          <div v-if="previousQuiz" class="row no-gutters">
            <div class="col">
              <span>{{ $t('messages.previousQuiz') }}&nbsp;👉&nbsp;</span>
              <strong><router-link class="no-decoration" :to="{ name: 'quiz-detail', params: { quizId: previousQuiz.id } }">{{ previousQuiz.name }}</router-link></strong>
            </div>
          </div>
        </section>
      </div>
    </div>

    <div v-if="quiz && quizStep === 0">
      <button id="quiz-start-btn" class="btn btn-lg btn-primary margin-10" @click="incrementStep()">▶️&nbsp;{{ $t('messages.startQuiz') }}</button>
    </div>

    <!-- Quiz en cours -->

    <div id="scroll-to-question" class="scroll-to-fix" style="height:0px"></div>

    <section v-if="quiz && (quizStep > 0) && quiz.questions[quizStep-1]">
      <QuestionAnswerCards v-bind:question="quiz.questions[quizStep-1]" v-bind:context="{ question_number: quizStep+' / '+quiz.questions.length, source: 'quiz' }" @answer-submitted="onAnswerSubmitted" />
      <button v-if="showNextButton && (quizStep < quiz.questions.length)" class="btn" :class="emphasisNextButton ? 'btn-primary' : 'btn-outline-primary'" @click="incrementStep()">⏩&nbsp;{{ $t('messages.nextQuestion') }}</button>
      <button v-if="showNextButton && (quizStep === quiz.questions.length)" class="btn btn-lg btn-primary" @click="incrementStep()">⏩&nbsp;{{ $t('messages.endQuiz') }}</button>
    </section>

    <!-- Quiz terminé -->

    <div id="scroll-to-results" class="scroll-to-fix" style="height:0px"></div>

    <section v-if="quiz && (quizStep > quiz.questions.length)">

      <section class="question">
        <h2>{{ $t('messages.yourScore') }} : <strong>{{ finalScore }} / {{ quiz.questions.length }}</strong></h2>

        <p>
          📈&nbsp;{{ $t('messages.quizCompletedStats') }} <strong>{{ quizStats.answer_count }}</strong> {{ $t('words.times') }}.<br />
          {{ $t('messages.quizCompletedBetter1') }} <strong>{{ finalScoreBetterThanPercent }}%</strong> {{ $t('messages.quizCompletedBetter2') }}
          <abbr v-bind:title="'dernière mise à jour le ' + statsLastUdated">stats&nbsp;?&nbsp;</abbr>
        </p>

        <div v-if="quiz.conclusion" v-html="quiz.conclusion" title="Conclusion du quiz"></div>
      </section>

      <ShareBox type="quiz" :quizName="quiz.name" :score="finalScore + '/' + quiz.questions.length" />

      <FeedbackCard v-bind:context="{ source: 'quiz', item: quiz }" />

      <!-- Next / similar quiz -->
      <section v-if="nextQuiz">
        <br />
        <h2 class="special-title">{{ $t('messages.nextQuiz') }}&nbsp;⏩</h2>
        <div class="row">
          <div class="col-sm-4">
            <QuizCard :quiz="nextQuiz" />
          </div>
        </div>
      </section>
      <section v-if="similarQuizs">
        <br />
        <h2 class="special-title">{{ $t('messages.similarQuiz') }}<span v-if="similarQuizs.length > 1">s</span>&nbsp;👯</h2>
        <div class="row">
          <div class="col-sm-4" v-for="quiz in similarQuizs" :key="quiz.id">
            <QuizCard :quiz="quiz" />
          </div>
        </div>
      </section>

    </section>
  </section>
</template>

<script>
import constants from '../constants';
import { metaTagsGenerator } from '../utils';
import QuizCard from '../components/QuizCard.vue';
import QuestionAnswerCards from '../components/QuestionAnswerCards.vue';
import FeedbackCard from '../components/FeedbackCard.vue';
import ShareBox from '../components/ShareBox.vue';

export default {
  name: 'QuizDetailPage',
  metaInfo() {
    // const url = `/quiz/${this.$route.params.quizId}`;
    const title = this.quiz && this.quiz.name ? `Quiz ${this.quiz.name}` : `Quiz #${this.$route.params.quizId}`;
    const description = this.quiz && this.quiz.introduction ? this.quiz.introduction : '';
    const imageUrl = this.quiz && this.quiz.image_background_url ? this.quiz.image_background_url : 'https://quizanthropocene.fr/showyourstripes_globe_1850-2019.png';
    return {
      title,
      meta: metaTagsGenerator(title, description, imageUrl),
    };
  },
  components: {
    QuizCard,
    QuestionAnswerCards,
    FeedbackCard,
    ShareBox,
  },

  data() {
    return {
      // quiz: null,
      quizStep: 0,
      showNextButton: true,
      emphasisNextButton: false,
      showQuizQuestions: false,
      quizStartTime: null,
      // quizRelationships: null,
      // previousQuiz: null,
      // nextQuiz: null,
    };
  },

  computed: {
    quiz() {
      let quiz = this.$store.getters.getQuizById(parseInt(this.$route.params.quizId, 10));
      // .slice(0) ? // .slice makes a copy of the array, instead of mutating the orginal
      // if the quiz is not found with its id, try with its slug
      if (!quiz) {
        quiz = this.$store.getters.getQuizBySlug(this.$route.params.quizId);
      }
      return quiz;
    },
    quizStats() {
      const quizStats = this.$store.getters.getQuizStatsById(this.quiz.id);
      // .slice(0) ? // .slice makes a copy of the array, instead of mutating the orginal
      return quizStats;
    },
    quizRelationships() {
      const quizRelationships = this.$store.getters.getQuizRelationshipsById(this.quiz.id);
      // .slice(0) ? // .slice makes a copy of the array, instead of mutating the orginal
      return quizRelationships;
    },
    previousQuiz() {
      const previousQuizRelationship = this.quizRelationships.find((qr) => (qr.to_quiz === this.quiz.id) && (qr.status === constants.QUIZ_RELATIONSHIP_NEXT));
      if (previousQuizRelationship) {
        return this.$store.getters.getQuizById(previousQuizRelationship.from_quiz);
      }
      return null;
    },
    nextQuiz() {
      const nextQuizRelationship = this.quizRelationships.find((qr) => (qr.from_quiz === this.quiz.id) && (qr.status === constants.QUIZ_RELATIONSHIP_NEXT));
      if (nextQuizRelationship) {
        return this.$store.getters.getQuizById(nextQuizRelationship.to_quiz);
      }
      return null;
    },
    similarQuizs() {
      const similarQuizRelationships = this.quizRelationships.filter((qr) => (qr.to_quiz === this.quiz.id) || (qr.from_quiz === this.quiz.id))
        .filter((qr) => (qr.status === constants.QUIZ_RELATIONSHIP_SIMILAR) || (qr.status === constants.QUIZ_RELATIONSHIP_TWIN));
      if (similarQuizRelationships.length) {
        const similarQuizRelationshipsIdList = similarQuizRelationships.map((qr) => ((qr.to_quiz === this.quiz.id) ? qr.from_quiz : qr.to_quiz));
        return this.$store.getters.getQuizzesByIdList(similarQuizRelationshipsIdList);
      }
      return null;
    },
    finalScore() {
      return this.quiz.questions.filter((q) => q.success).length;
    },
    finalScoreBetterThanPercent() {
      const finalScoreBetterThan = this.quizStats.answer_success_count_split.filter((q) => (q.answer_success_count < this.finalScore)).reduce((acc, curr) => acc + curr.count, 0);
      const finalScoreBetterThanPercent = this.quizStats.answer_count ? Math.round((finalScoreBetterThan / this.quizStats.answer_count) * 100) : 0;
      return finalScoreBetterThanPercent;
    },
    statsLastUdated() {
      return new Date(constants.DATA_LAST_UPDATED_DATETIME).toLocaleDateString('fr-FR', {
        year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', hour12: false,
      });
    },
    currentLocale() {
      return this.$store.state.locale;
    },
  },

  beforeRouteUpdate(to, from, next) {
    // reloading a quiz when moving from one to another
    if (from.path !== to.path) {
      this.initQuiz();
    }
    next();
  },

  watch: {
    // eslint-disable-next-line
    'quiz' (newQuiz, oldQuiz) {
      if (newQuiz) {
        this.adaptLocale();
      }
    },
  },

  mounted() {
  },

  methods: {
    adaptLocale() {
      if (this.quiz && this.$store.state.locale && this.quiz.language !== this.$store.state.locale.value) {
        this.$i18n.locale = constants.LANGUAGE_CHOICE_LIST.find((l) => l.value === this.quiz.language).key;
      }
    },
    initQuiz() {
      this.quizStep = 0;
      this.showQuizQuestions = false;
    },
    incrementStep() {
      // first step ?
      if (this.quizStep === 0) {
        this.quizStartTime = window.performance.now();
      }

      // increment quiz step
      this.quizStep += 1;
      this.showNextButton = false;
      setTimeout(() => {
        // why scroll to this div and not to 'answer' directly ? To have a slight top margin
        document.getElementById('scroll-to-question').scrollIntoView({ behavior: 'smooth' });
      }, 25);

      // done ?
      if (this.quizStep > this.quiz.questions.length) {
        this.submitQuiz();
        setTimeout(() => {
          // why scroll to this div and not to 'answer' directly ? To have a slight top margin
          document.getElementById('scroll-to-results').scrollIntoView({ behavior: 'smooth' });
        }, 25);
      }
    },
    onAnswerSubmitted(data) {
      this.quiz.questions[this.quizStep - 1].success = data.success;
      this.showNextButton = true;
      this.emphasisNextButton = true;
    },
    submitQuiz() {
      // stats
      const quizEndTime = window.performance.now();
      const quizDurationInSeconds = Math.round((quizEndTime - this.quizStartTime) / 1000);
      fetch(`${process.env.VUE_APP_STATS_ENDPOINT}/quiz-answer-event`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          quiz: this.quiz.id,
          answer_success_count: this.quiz.questions.filter((q) => q.success).length,
          duration_seconds: quizDurationInSeconds,
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
}

.row > .col-lg-4,
.row > .col-sm-6 {
  padding-bottom: 15px;
}

@media(hover: hover) and (pointer: fine) {
  .row-item-question:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
  }
}
</style>
