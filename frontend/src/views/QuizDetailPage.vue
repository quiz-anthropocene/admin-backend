<template>
  <section>

    <!-- Quiz header -->
    <div v-if="quiz" class="card">
      <img v-bind:src="quiz.image_background_url || 'https://showyourstripes.info/stripes/GLOBE---1850-2019-MO.png'" class="image-background" :class="(quizStep === 0) ? 'height-200' : 'height-50'">

      <div class="card-body">
        <h2 class="card-title"><span v-if="quizStep > 0">Quiz : </span>{{ quiz.name }}</h2>

        <section v-if="(quizStep === 0) || (quizStep > quiz.questions.length)">
          <div class="card-subtitle" v-html="quiz.introduction" title="Introduction du quiz"></div>

          <hr class="margin-top-bottom-10" />

          <div class="row no-gutters small">
            <div class="col" title="Nombre de questions">
              ❓&nbsp;<span class="label label-hidden"><strong>{{ quiz.questions.length }}</strong></span>Questions
            </div>
            <div class="col" title="Difficulté">
              🏆&nbsp;Difficulté<span class="label label-hidden"><strong>{{ quiz.difficulty_average | round(1) }} / 4</strong></span>
            </div>
            <div class="col" title="Auteur du quiz">
              📝&nbsp;Auteur<span class="label label-hidden"><strong>{{ quiz.author }}</strong></span>
            </div>
            <!-- <span title="Date de création du quiz">📊&nbsp;Crée le:&nbsp;{{ new Date(quiz.created).toLocaleString() }}</span> -->
          </div>

          <hr v-if="quiz.tags && quiz.tags.length > 0" class="margin-top-bottom-10" />

          <div v-if="quiz.tags && quiz.tags.length > 0" class="small" title="Tag(s) du quiz">
            🏷️&nbsp;<span v-for="(tag, index) in quiz.tags" :key="tag.id">
              <span v-if="index < 3" class="label label-tag">{{ tag.name }}</span>
            </span>
          </div>
        </section>
      </div>
    </div>

    <div v-if="quiz && quizStep === 0" class="quiz-start">
      <br />
      <button class="btn btn-lg btn-primary margin-5" @click="incrementStep()">⏩&nbsp;Commencer le quiz !</button>
    </div>

    <!-- Quiz en cours -->

    <section v-if="quiz && (quizStep > 0) && quiz.questions[quizStep-1]">
      <QuestionAnswerCards v-bind:question="quiz.questions[quizStep-1]" v-bind:context="{ question_number: quizStep+' / '+quiz.questions.length, source: 'quiz' }" @answer-submitted="onAnswerSubmitted" />
      <button v-if="showNextButton && (quizStep < quiz.questions.length)" class="btn" :class="emphasisNextButton ? 'btn-primary' : 'btn-outline-primary'" @click="incrementStep()">⏩&nbsp;Question suivante</button>
      <button v-if="showNextButton && (quizStep === quiz.questions.length)" class="btn btn-lg btn-primary" @click="incrementStep()">⏩&nbsp;C'est fini ! Voir vos résultats</button>
    </section>

    <!-- Quiz terminé -->

    <section v-if="quiz && (quizStep > quiz.questions.length)" class="question">
      <h2>Votre résultat : <strong>{{ quiz.questions.filter(q => q['success']).length }} / {{ quiz.questions.length }}</strong></h2>

      <div v-if="quiz.conclusion" v-html="quiz.conclusion" title="Conclusion du quiz"></div>

      <div class="row">
        <div class="col">
          <a class="fake-link" @click="showQuizQuestions = !showQuizQuestions">Afficher le détails de vos réponses</a>
          <span v-if="!showQuizQuestions">&nbsp;▸</span>
          <span v-if="showQuizQuestions">&nbsp;▾</span>
        </div>
      </div>

      <hr v-if="showQuizQuestions" />

      <div v-if="showQuizQuestions" class="row">
        <div class="col-lg-4 col-sm-6" v-for="question in quiz.questions" :key="question.id"><!-- :class="question.success ? 'answer-success' : 'answer-error'" -->
          <router-link class="no-decoration" :to="{ name: 'question-detail', params: { questionId: question.id } }">
            <QuestionPreviewCard v-bind:question="question" v-bind:customClass="question.success ? 'answer-success' : 'answer-error'" />
          </router-link>
        </div>
      </div>
    </section>

    <div v-if="quiz && (quizStep > quiz.questions.length)" class="alert alert-primary margin-0" role="alert">
      Partager le quiz : <strong id="quiz-share-url">{{ quizShareUrl }}</strong>
      <!-- <a class="fake-link float-right" @click="copyQuizShareUrlToClipboard()">📋&nbsp;Copier</a> -->
    </div>

    <FeedbackCard v-if="quiz && (quizStep > quiz.questions.length)" v-bind:context="{ source: 'quiz', item: quiz }" />
  </section>
</template>

<script>
import { metaTagsGenerator } from '../utils';
import QuestionAnswerCards from '../components/QuestionAnswerCards.vue';
import QuestionPreviewCard from '../components/QuestionPreviewCard.vue';
import FeedbackCard from '../components/FeedbackCard.vue';

export default {
  name: 'QuizDetailPage',
  metaInfo() {
    // const url = `/quiz/${this.$route.params.quizId}`;
    const title = this.quiz && this.quiz.name ? `Quiz #${this.$route.params.quizId} - ${this.quiz.name}` : `Quiz #${this.$route.params.quizId}`;
    const description = this.quiz && this.quiz.introduction ? this.quiz.introduction : 'Le quiz n’a pas de description';
    const imageUrl = this.quiz && this.quiz.image_background_url ? this.quiz.image_background_url : 'https://showyourstripes.info/stripes/GLOBE---1850-2019-MO.png';
    return {
      title,
      meta: metaTagsGenerator(title, description, imageUrl),
    };
  },
  components: {
    QuestionAnswerCards,
    QuestionPreviewCard,
    FeedbackCard,
  },

  data() {
    return {
      // quiz: null,
      quizStep: 0,
      showNextButton: true,
      emphasisNextButton: false,
      showQuizQuestions: false,
    };
  },

  computed: {
    quiz() {
      const quiz = this.$store.getters.getQuizById(parseInt(this.$route.params.quizId, 10));
      // .slice(0) ? // .slice makes a copy of the array, instead of mutating the orginal
      if (quiz) { // can be undefined if loading '/quiz/<quizId' page directly
        quiz.questions.sort(() => Math.random() - 0.5); // random order
      }
      return quiz;
    },
    quizShareUrl() {
      return window.location.origin + this.$route.path;
    },
  },

  mounted() {
  },

  methods: {
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
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/quizzes/${this.quiz.id}/answer-events`, {
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
    // copyQuizShareUrlToClipboard() {
    //   let quizShareUrlElement = document.querySelector('#quiz-share-url');
    //   console.log(quizShareUrlElement, quizShareUrlElement.text)
    //   // quizShareUrlElement.setAttribute('type', 'text');
    //   quizShareUrlElement.innerText.select();
    //   document.execCommand('copy');
    // }
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

.image-background {
  /* height: 200px; */
  width: 100%;
  object-fit: cover;
  text-align: center;
}
.height-200 {
  height: 200px;
}
.height-50 {
  height: 50px;
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
