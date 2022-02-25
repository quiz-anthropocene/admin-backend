<template>
  <section>

    <h2 class="text-align-left">
      Des questions-réponses sur notre empreinte sur la planète
    </h2>

    <p class="text-align-left">
      Dérèglement du climat, anéantissement du vivant, épuisement des ressources naturelles, artificialisation des espaces naturels…
      Nous voilà entrés dans l’Anthropocène, l’ère de l’humain. L’homme est devenu la plus grande force qui façonne le monde.
    </p>
    <p class="text-align-left">
      Ce site a vocation à vous en donner un premier aperçu. {{ questionsCount }} questions en ligne, regroupées en {{ quizzesPublishedCount }} quiz thématiques, avec des explications, des liens fiables pour aller plus loin et des illustrations.
      Déjà {{ question_answer_count_formatted }} questions jouées sur le site.
    <p class="text-align-left margin-bottom-0">
      A vous de tester, et faire tourner !
    </p>

    <br />

    <!-- <div class="alert alert-success" role="alert">
      Le Quiz de l'Anthropocène a maintenant son atelier !
      <span class="no-wrap">➡️&nbsp;<router-link :to="{ name: 'atelier' }"><strong>Plus d'informations</strong></router-link>&nbsp;⬅️</span>
    </div> -->

    <h2 v-if="quizzesSpotlighted && quizzesSpotlighted.length > 0" class="text-align-left">
      ✨&nbsp;{{ $t('messages.recentQuizs') }}
    </h2>
    <div class="row" v-if="quizzesSpotlighted && quizzesSpotlighted.length > 0" id="quiz-list">
      <div class="col-sm-4" v-for="quiz in quizzesSpotlighted" :key="quiz.id">
        <QuizCard :quiz="quiz" />
      </div>
      <div class="col-sm-4 my-auto">
        <router-link class="no-decoration" :to="{ name: 'quiz-list' }">
            <button id="all-quizs-btn" class="btn btn-primary btn-lg">
            🕹&nbsp;<strong>{{ $t('messages.allQuizs') }}</strong>&nbsp;
            <small>({{ quizzesPublishedCount }})</small>
          </button>
        </router-link>
      </div>
    </div>

    <br />

    <div class="jumbotron jumbotron-fluid">
      <div class="container">
        <div class="row">
          <div class="col-sm padding-top-bottom-15">
            <svg class="bi bi-clipboard-data text-primary" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M4 1.5H3a2 2 0 00-2 2V14a2 2 0 002 2h10a2 2 0 002-2V3.5a2 2 0 00-2-2h-1v1h1a1 1 0 011 1V14a1 1 0 01-1 1H3a1 1 0 01-1-1V3.5a1 1 0 011-1h1v-1z" clip-rule="evenodd"/>
              <path fill-rule="evenodd" d="M9.5 1h-3a.5.5 0 00-.5.5v1a.5.5 0 00.5.5h3a.5.5 0 00.5-.5v-1a.5.5 0 00-.5-.5zm-3-1A1.5 1.5 0 005 1.5v1A1.5 1.5 0 006.5 4h3A1.5 1.5 0 0011 2.5v-1A1.5 1.5 0 009.5 0h-3z" clip-rule="evenodd"/>
              <path d="M4 11a1 1 0 112 0v1a1 1 0 11-2 0v-1zm6-4a1 1 0 112 0v5a1 1 0 11-2 0V7zM7 9a1 1 0 012 0v3a1 1 0 11-2 0V9z"/>
            </svg>
            <h3>
              {{ $t('home.item1Title') }}<br />
              <small>{{ $t('home.item1Subtitle') }}</small>
            </h3>
          </div>
          <div class="col-sm padding-top-bottom-15">
            <svg class="bi bi-tag text-secondary" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M.5 2A1.5 1.5 0 012 .5h4.586a1.5 1.5 0 011.06.44l7 7a1.5 1.5 0 010 2.12l-4.585 4.586a1.5 1.5 0 01-2.122 0l-7-7A1.5 1.5 0 01.5 6.586V2zM2 1.5a.5.5 0 00-.5.5v4.586a.5.5 0 00.146.353l7 7a.5.5 0 00.708 0l4.585-4.585a.5.5 0 000-.708l-7-7a.5.5 0 00-.353-.146H2z" clip-rule="evenodd"/>
              <path fill-rule="evenodd" d="M2.5 4.5a2 2 0 114 0 2 2 0 01-4 0zm2-1a1 1 0 100 2 1 1 0 000-2z" clip-rule="evenodd"/>
            </svg>
            <h3 v-html="$t('home.item2Title')"></h3>
          </div>
          <div class="col-sm padding-top-bottom-15">
            <svg class="bi bi-arrow-repeat text-success" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M2.854 7.146a.5.5 0 00-.708 0l-2 2a.5.5 0 10.708.708L2.5 8.207l1.646 1.647a.5.5 0 00.708-.708l-2-2zm13-1a.5.5 0 00-.708 0L13.5 7.793l-1.646-1.647a.5.5 0 00-.708.708l2 2a.5.5 0 00.708 0l2-2a.5.5 0 000-.708z" clip-rule="evenodd"/>
              <path fill-rule="evenodd" d="M8 3a4.995 4.995 0 00-4.192 2.273.5.5 0 01-.837-.546A6 6 0 0114 8a.5.5 0 01-1.001 0 5 5 0 00-5-5zM2.5 7.5A.5.5 0 013 8a5 5 0 009.192 2.727.5.5 0 11.837.546A6 6 0 012 8a.5.5 0 01.501-.5z" clip-rule="evenodd"/>
            </svg>
            <h3>
              {{ $t('home.item3Title') }}<br />
              <small>{{ $t('home.item3Subtitle') }} <router-link :to="{ name: 'contribute' }">contributions</router-link> !</small>
            </h3>
          </div>
        </div>
      </div>
    </div>

    <div class="alert alert-primary" role="alert">
      <i>
        {{ $t('home.thereIsCurrently') }} <strong>{{ questionsCount }} questions</strong> {{ $t('words.et') }} <strong>{{ quizzesPublishedCount }} quiz</strong>.
        <router-link :to="{ name: 'about' }">{{ $t('home.helpUs') }}</router-link> {{ $t('home.toAddMore') }}{{ $t('words.exclamationMark') }}
      </i>
    </div>
    <div v-if="newsletterRegistrationCallback" class="alert alert-success" role="alert">
      {{ $t('newsletter.success') }}
      <button type="button" class="close" data-dismiss="alert" aria-label="Close" @click="newsletterCleanup()">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>

    <br />

    <div class="row">
      <div class="col-sm-8 offset-sm-2">
        <h3>
          Une <i>newsletter</i> pour vous tenir au courant des nouveautés
        </h3>
        <p>
          On vous enverra juste quelques emails dans l'année, pour vous annoncer de nouveaux quizs, des partenariats, etc.
        </p>
        <form class="row" @submit.prevent="submitNewsletterRegistration" v-if="!newsletterRegistrationLoading && !newsletterRegistrationSuccess && !newsletterRegistrationError">
          <div class="col-sm-8">
            <div class="form-group">
              <input type="email" id="newsletter_email" class="form-control" placeholder="Votre email" v-model="emailNewsletterRegistration" required />
            </div>
          </div>
          <div class="col-sm-4 text-align-left">
            <button id="newsletter-btn" class="btn btn-primary" type="submit" :disabled="!emailNewsletterRegistration">Je m'inscris !</button>
          </div>
        </form>
        <div v-if="newsletterRegistrationLoading">
          Inscription en cours...
        </div>
        <div class="alert alert-success" v-if="newsletterRegistrationSuccess">
          Merci pour votre inscription ! 💯
        </div>
        <div class="alert alert-danger" v-if="newsletterRegistrationError">
          Une erreur s'est produite au moment de votre inscription 😢
          <span class="fake-link" @click="newsletterCleanup()">Réessayer</span>
        </div>
      </div>
    </div>

  </section>
</template>

<script>
import QuizCard from '../components/QuizCard.vue';

export default {
  name: 'HomePage',
  components: {
    QuizCard,
  },
  data() {
    return {
      // questionSameFilterNextId: null,
      emailNewsletterRegistration: null,
      newsletterRegistrationLoading: null,
      newsletterRegistrationSuccess: null,
      newsletterRegistrationError: null,
      newsletterRegistrationCallback: null,
    };
  },

  computed: {
    quizzesPublishedCount() {
      return this.$store.state.quizzesPublished.length;
    },
    questionsCount() {
      return this.$store.state.questionsValidated.length;
    },
    quizzesSpotlighted() {
      return this.$store.state.quizzesSpotlighted;
    },
    question_answer_count_formatted() {
      return Intl.NumberFormat('fr-FR').format(this.$store.state.stats.question_answer_count || 250000);
    },
  },

  // watch: {
  //   questionsCount: {
  //     immediate: true,
  //     // eslint-disable-next-line
  //     handler(newQuestionsCount, oldQuestionsCount) {
  //       if (newQuestionsCount) {
  //         this.questionSameFilterNextId = this.$store.getters.getNextQuestionByFilter().id;
  //       }
  //     },
  //   },
  // },

  mounted() {
    if (this.$route.query.newsletter) {
      this.newsletterRegistrationCallback = true;
    }
  },

  methods: {
    submitNewsletterRegistration() {
      this.newsletterRegistrationLoading = true;
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/newsletter`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: this.emailNewsletterRegistration,
        }),
      })
        .then((response) => {
          this.newsletterRegistrationLoading = false;
          return response.json();
        })
      // eslint-disable-next-line
      .then(data => {
          console.log(data);
          if (data.includes('Erreur')) {
            this.newsletterRegistrationError = data;
          } else {
            this.newsletterRegistrationSuccess = data;
          }
        })
        .catch((error) => {
          console.log(error);
          this.newsletterRegistrationLoading = false;
          this.newsletterRegistrationError = error;
        });
    },
    newsletterCleanup() {
      this.newsletterRegistrationLoading = null;
      this.newsletterRegistrationSuccess = null;
      this.newsletterRegistrationError = null;
      this.newsletterRegistrationCallback = null;
    },
  },
};
</script>

<style scoped>
svg {
  font-size: 2em;
}

.jumbotron {
  padding-top: 1em;
  padding-bottom: 1em;
  margin-bottom: 1em;
}
.jumbotron .row .col:hover {
  transform: scale(1.03);
}

.row > .col-sm-4,
.row > .col-sm-3 {
  padding-bottom: 15px;
}
.row > .col-sm-4 > .card,
.row > .col-sm-3 > .card {
  height: 100%;
}
</style>
