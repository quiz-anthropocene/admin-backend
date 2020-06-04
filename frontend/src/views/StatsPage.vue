<template>
  <section class="text-align-left">
    <h2>Quelques statistiques</h2>
    
    <h3>❓&nbsp;Questions</h3>
    <p>
      Il y a actuellement <strong v-if="questionPublishCount">{{ questionPublishCount }}</strong> questions publiées,
      et <strong>{{ questionValidationStatusInProgressCount ? questionValidationStatusInProgressCount : 0 }}</strong> en cours de validation.
    </p>

    <br />
    <h3>🕹️&nbsp;Quiz</h3>
    <p>
      <strong>{{ quiz_count ? quiz_count : 0 }}</strong> quiz ont été créés.
    </p>

    <br />
    <h3>🔗&nbsp;Réponses</h3>
    <p>
      L'application totalise <strong>{{ questionAnswerCountStats }}</strong> réponses (depuis la mise en ligne en Mars 2020).
    </p>

    <br />
    <h3>📂&nbsp;Catégories</h3>
    Questions par catégories:
    <ul>
      <li v-for="category in categories" :key="category.name">
        {{ category.name }}: <strong>{{ category.question_count }}</strong>
      </li>
    </ul>

    <br />
    <h3>🏷️&nbsp;Tags</h3>
    Questions par tags:
    <ul>
      <li v-for="tag in tags" :key="tag.name">
        {{ tag.name }}: <strong>{{ tag.question_count }}</strong>
      </li>
    </ul>

    <br />
    <h3>✍️&nbsp;Auteurs</h3>
    Questions par auteurs:
    <ul>
      <li v-for="author in authors" :key="author.name">
        {{ author.name }}: <strong>{{ author.question_count }}</strong>
      </li>
    </ul>

  </section>
</template>

<script>
export default {
  name: 'StatsPage',
  components: {
  },

  data() {
    return {
      questionPublishCount: null,
      questionValidationStatusInProgressCount: null,
      quizPublishStats: null,
      questionAnswerCountStats: null,
      questionCategoryStats: null,
      questionTagStats: null,
      questionAuthorStats: null,
      // questionAnswerStats: null,
      loading: false,
      error: null,
    }
  },

  computed: {
    quiz_count () {
      return this.$store.state.quizzes.length;
    },
    categories () {
      return this.$store.state.categories
        .filter(c => c.question_count)
        .sort((a, b) => b.question_count - a.question_count);
    },
    tags () {
      return this.$store.state.tags
        .filter(t => t.question_count)
        .sort((a, b) => b.question_count - a.question_count);
    },
    authors () {
      return this.$store.state.authors
        .filter(a => a.question_count)
        .sort((a, b) => b.question_count - a.question_count);
    },
  },

  mounted () {
    this.fetchQuestionStats();
  },

  methods: {
    fetchQuestionStats() {
      this.error = this.question = null;
      this.loading = true;
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/stats`)
        .then(response => {
          this.loading = false
          return response.json()
        })
        .then(data => {
          this.questionPublishCount = data["question_publish_count"];
          this.questionValidationStatusInProgressCount = data["question_validation_status_in_progress_count"];
          this.questionAnswerCountStats = data["answer_count"];
          // this.questionAnswerStats = data["answer"];
          
        })
        .catch(error => {
          console.log(error)
          this.error = error;
        })
    },

  }
}
</script>
