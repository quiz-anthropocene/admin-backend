<template>
  <section>
    <br />

    <h2>
      <router-link class="no-decoration" :to="{ name: 'quiz-list' }">Quiz:</router-link>&nbsp;
      <span v-if="quiz" class="text-secondary">{{ quiz.name }}</span>
    </h2>

    <div v-if="quiz && quiz.questions && quiz.questions.length > 0">
      <strong>{{ quiz.questions.length }}</strong> question<span v-if="quiz.questions.length > 1">s</span>
    </div>

    <div v-if="quiz" class="row margin-top-bottom-10 small">
      <div v-if="quiz.categories_list && quiz.categories_list.length > 0" title="Catégorie(s) du quiz">🏷️&nbsp;Catégorie<span v-if="quiz.categories_list.length > 1">s</span>:&nbsp;{{ quiz.categories_list.join(', ') }}</div>
      <!-- <div v-if="quiz.tags && quiz.tags.length > 0" title="Tag(s) du quiz">🏷️&nbsp;Tag<span v-if="quiz.tags.length > 1">s</span>:&nbsp;{{ quiz.tags.join(', ') }}</div> -->
      <div title="Difficulté">&nbsp;Difficulté:&nbsp;{{ quiz.difficulty_average }}</div>
      <div title="Auteur du quiz">📝&nbsp;Auteur:&nbsp;{{ quiz.author }}</div>
      <!-- <div title="Date de création du quiz">📊&nbsp;Crée le:&nbsp;{{ new Date(quiz.created).toLocaleString() }}</div> -->
    </div>

    <hr />

    <section v-if="quiz && quizStep === 0">
      <button class="btn btn-outline-primary" @click="incrementStep()">⏩&nbsp;Commencer le quiz !</button>
    </section>


    <!-- Quiz en cours -->

    <section v-if="quiz && (quizStep > 0) && quiz.questions[quizStep-1]">
      <QuestionAnswerCards v-bind:question="quiz.questions[quizStep-1]" v-bind:context="{ question_number: quizStep+' / '+quiz.questions.length, source: 'quiz' }" @answerSubmitted="answerSubmitted($event)" />
      <br />
      <button v-if="showNextButton && (quizStep < quiz.questions.length)" class="btn btn-outline-primary" @click="incrementStep()">⏩&nbsp;Question suivante</button>
      <button v-if="showNextButton && (quizStep === quiz.questions.length)" class="btn btn-outline-primary" @click="incrementStep()">⏩&nbsp;Voir vos résultats</button>
    </section>


    <!-- Quiz terminé -->

    <section v-if="quiz && (quizStep > quiz.questions.length)">
      <h2>C'est terminé !</h2>
      <h3>Vos résultats: {{ quiz.questions.filter(q => q['success']).length }} / {{ quiz.questions.length }}</h3>
      <br />
      <a href="#" @click="showQuizQuestions = !showQuizQuestions">Afficher les questions</a>
      <br />
    </section>

    <hr v-if="showQuizQuestions" />

    <section v-if="showQuizQuestions">
      <div class="row">
        <div class="row-item row-item-question" v-for="question in quiz.questions" :key="question.id" :class="question.success ? 'answer-success' : 'answer-error'">
          <router-link class="no-decoration" :to="{ name: 'question-detail', params: { questionId: question.id } }">
            <QuestionPreviewCard v-bind:question="question" />
          </router-link>
        </div>
      </div>
    </section>

    <br />
    <hr v-if="quiz && (quizStep > quiz.questions.length)" />
    <div v-if="quiz && (quizStep > quiz.questions.length)" class="row actions">
      <div class="col-sm">
        <router-link :to="{ name: 'contribute' }">
          ✍️&nbsp;Ajouter une question
        </router-link>
      </div>
      <div class="col-sm">
        <router-link :to="{ name: 'quiz-list' }">
          🕹️&nbsp;Tous les quiz
        </router-link>
      </div>
      <div class="col-sm">
        <HomeLink />
      </div>
    </div>
  </section>
</template>

<script>
import QuestionAnswerCards from '../components/QuestionAnswerCards.vue'
import QuestionPreviewCard from '../components/QuestionPreviewCard.vue'
import HomeLink from '../components/HomeLink.vue'

export default {
  name: 'QuizDetailPage',
  components: {
    QuestionAnswerCards,
    QuestionPreviewCard,
    HomeLink
  },

  data () {
    return {
      // quiz: null,
      quizStep: 0,
      showNextButton: true,
      showQuizQuestions: false,
    }
  },

  computed: {
    quiz () {
      return this.$store.getters.getQuizById(this.$route.params.quizId);
    },
  },

  mounted () {
  },

  methods: {
    incrementStep () {
      // increment quiz step
      this.quizStep += 1;
      this.showNextButton = false;

      // done ?
      if (this.quizStep > this.quiz.questions.length) {
        this.submitQuiz();
      }
    },
    answerSubmitted(data) {
      this.quiz.questions[this.quizStep-1]['success'] = data['success'];
      this.showNextButton = true;
    },
    submitQuiz() {
      // stats
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/quizzes/${this.quiz.id}/stats`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          answer_success_count: this.quiz.questions.filter(q => q['success']).length
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
.row-item-question {
  height: 150px;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: 0.1s;
  border: 2px solid var(--primary);
  border-radius: 5px;
  overflow: hidden;
  cursor: pointer;
}
.answer-success {
  border-color: green;
  background-color: #f2f8f2;
}
.answer-error {
  border-color: red;
  background-color: #fff2f2;
}

@media(hover: hover) and (pointer: fine) {
  .row-item-question:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
  }
}
</style>
