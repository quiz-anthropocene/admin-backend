<template>
  <section>

    <!-- Quiz header -->
    <div v-if="quiz" class="card">
      <img v-bind:src="quiz.image_background_url || 'https://quizanthropocene.fr/showyourstripes_globe_1850-2019.png'" class="card-img-top" :class="(quizStep === 0) ? 'height-150' : 'height-50'">

      <div class="card-body">
        <h2 class="card-title">
          Quiz{{ $t('words.semiColon') }} {{ quiz.name }}
          <span v-if="quiz.has_audio" class="label small" style="vertical-align:top">🔉{{ $t('messages.audioComments') }}</span>
        </h2>

        <section v-if="(quizStep === 0) || (quizStep > quiz.questions.length)">
          <div class="card-subtitle" v-html="quiz.introduction" title="Introduction du quiz"></div>

          <hr class="margin-top-bottom-10" />

          <div class="row no-gutters small">
            <div class="col" title="Nombre de questions">
              <span class="label label-hidden"><strong>{{ quiz.questions.length }}</strong></span>Questions
            </div>
            <div class="col" v-bind:title="$t('messages.difficulty')">
              🏆&nbsp;{{ $t('messages.difficulty') }}<span class="label label-hidden"><strong>{{ quiz.difficulty_average | round(1) }} / 4</strong></span>
            </div>
            <!-- <div class="col" title="Auteur du quiz">
              📝&nbsp;Auteur<span class="label label-hidden"><strong>{{ quiz.author }}</strong></span>
            </div> -->
            <!-- <span title="Date de création du quiz">📊&nbsp;Crée le:&nbsp;{{ new Date(quiz.created).toLocaleString() }}</span> -->
            <div v-if="quiz.tags && quiz.tags.length > 0" class="col small" title="Tag(s) du quiz">
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

    <section v-if="quiz && (quizStep > 0) && quiz.questions[quizStep-1]">
      <QuestionAnswerCards v-bind:question="quiz.questions[quizStep-1]" v-bind:context="{ question_number: quizStep+' / '+quiz.questions.length, source: 'quiz' }" @answer-submitted="onAnswerSubmitted" />
      <button v-if="showNextButton && (quizStep < quiz.questions.length)" class="btn" :class="emphasisNextButton ? 'btn-primary' : 'btn-outline-primary'" @click="incrementStep()">⏩&nbsp;{{ $t('messages.nextQuestion') }}</button>
      <button v-if="showNextButton && (quizStep === quiz.questions.length)" class="btn btn-lg btn-primary" @click="incrementStep()">⏩&nbsp;{{ $t('messages.endQuiz') }}</button>
    </section>

    <!-- Quiz terminé -->

    <section v-if="quiz && (quizStep > quiz.questions.length)">

      <section class="question">
        <h2>{{ $t('messages.yourScore') }} : <strong>{{ finalScore }} / {{ quiz.questions.length }}</strong></h2>

        <p>
          📈&nbsp;{{ $t('messages.quizCompletedStats') }} <strong>{{ quizStats.answer_count }}</strong> {{ $t('words.times') }}.<br />
          {{ $t('messages.quizCompletedBetter1') }} <strong>{{ finalScoreBetterThanPercent }}%</strong> {{ $t('messages.quizCompletedBetter2') }}
        </p>

        <div v-if="quiz.conclusion" v-html="quiz.conclusion" title="Conclusion du quiz"></div>
      </section>

      <ShareBox type="quiz" :quizName="quiz.name" :score="finalScore + '/' + quiz.questions.length" />

      <FeedbackCard v-bind:context="{ source: 'quiz', item: quiz }" />

      <!-- Next / similar quiz -->
      <section v-if="nextQuiz">
        <br />
        <h2 class="special-title">{{ $t('messages.nextQuiz') }}&nbsp;⏩</h2>
        <QuizCard :quiz="nextQuiz" />
      </section>

      <section v-if="similarQuizs">
        <br />
        <h2 class="special-title">{{ $t('messages.similarQuiz') }}<span v-if="similarQuizs.length > 1">s</span>&nbsp;👯</h2>
        <QuizCard v-for="quiz in similarQuizs" :key="quiz.id" :quiz="quiz" />
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
    const title = this.quiz && this.quiz.name ? `Quiz #${this.$route.params.quizId} - ${this.quiz.name}` : `Quiz #${this.$route.params.quizId}`;
    const description = this.quiz && this.quiz.introduction ? this.quiz.introduction : 'Le quiz n’a pas de description';
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
      // quizRelationships: null,
      // previousQuiz: null,
      // nextQuiz: null,
    };
  },

  computed: {
    quiz() {
      const quiz = this.$store.getters.getQuizById(parseInt(this.$route.params.quizId, 10));
      // .slice(0) ? // .slice makes a copy of the array, instead of mutating the orginal
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
  },

  beforeRouteUpdate(to, from, next) {
    // reloading a quiz when moving from one to another
    if (from.path !== to.path) {
      this.initQuiz();
    }
    next();
  },

  mounted() {
  },

  methods: {
    initQuiz() {
      this.quizStep = 0;
      this.showQuizQuestions = false;
    },
    incrementStep() {
      // increment quiz step
      this.quizStep += 1;
      this.showNextButton = false;

      // done ?
      if (this.quizStep > this.quiz.questions.length) {
        this.submitQuiz();
      }
    },
    onAnswerSubmitted(data) {
      this.quiz.questions[this.quizStep - 1].success = data.success;
      this.showNextButton = true;
      this.emphasisNextButton = true;
    },
    submitQuiz() {
      // stats
      fetch(`${process.env.VUE_APP_STATS_ENDPOINT}/quizzes/${this.quiz.id}/answer-events`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          answer_success_count: this.quiz.questions.filter((q) => q.success).length,
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
